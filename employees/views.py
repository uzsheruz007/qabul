import json
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import QabulKomissiya, IshAriza, IshArizaFile
from .forms import IshArizaForm


class KomissiyaView(TemplateView):
    template_name = "komissiya.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rais'] = QabulKomissiya.objects.filter(lavozim_turi='rais', is_active=True).first()
        context['azolar'] = QabulKomissiya.objects.filter(is_active=True).exclude(lavozim_turi='rais')
        return context


def ish_ariza(request):
    if request.method == 'POST':
        form = IshArizaForm(request.POST, request.FILES)
        if form.is_valid():
            ariza = form.save()

            # Ko'p fayllarni saqlash
            file_fields = {
                'academic_title_diplomas': 'academic_title',
                'academic_degree_diplomas': 'academic_degree',
                'language_certs': 'language_cert',
                'work_references': 'work_reference',
            }
            for field_name, file_type in file_fields.items():
                for f in request.FILES.getlist(field_name):
                    IshArizaFile.objects.create(ariza=ariza, file_type=file_type, file=f)

            _send_telegram(ariza)
            _send_email(ariza)

            return redirect('ish_ariza_success')
    else:
        form = IshArizaForm()

    return render(request, 'ish_ariza.html', {'form': form})


def ish_ariza_success(request):
    return render(request, 'ish_ariza_success.html')


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update = json.loads(request.body)
            from .bot import handle_update
            handle_update(update)
        except Exception:
            pass
    return HttpResponse('OK')


# ── ichki yordamchi funksiyalar ──────────────────────────────────────────────

def _send_telegram(ariza):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    admin_ids = getattr(settings, 'TELEGRAM_ADMIN_IDS', None) or [getattr(settings, 'TELEGRAM_CHAT_ID', None)]
    admin_ids = [cid for cid in admin_ids if cid]
    if not token or not admin_ids:
        return

    millat = ariza.get_nationality_display()
    if ariza.nationality == 'other' and ariza.nationality_other:
        millat = ariza.nationality_other

    text = (
        "📋 *Yangi ish o'rni arizasi*\n\n"
        f"👤 *F.I.Sh:* {ariza.full_name}\n"
        f"📞 *Telefon:* {ariza.phone}\n"
        f"📧 *Email:* {ariza.email}\n"
        f"🌍 *Millat:* {millat}\n"
        f"🏠 *Manzil:* {ariza.address}\n"
        f"🎂 *Tug'ilgan sana:* {ariza.birth_date.strftime('%d.%m.%Y')}\n"
        f"🎓 *Ma'lumot:* {ariza.get_education_level_display()}\n"
        f"🏛 *Ta'lim muassasasi:* {ariza.institution}\n"
    )
    if ariza.academic_title:
        text += f"🏅 *Ilmiy unvon:* {ariza.academic_title}\n"
    if ariza.academic_degree:
        text += f"🔬 *Ilmiy daraja:* {ariza.academic_degree}\n"
    if ariza.foreign_language:
        text += f"🌐 *Xorijiy til:* {ariza.foreign_language}\n"
    text += f"\n🕐 *Vaqt:* {ariza.created_at.strftime('%d.%m.%Y %H:%M')}"

    base = f"https://api.telegram.org/bot{token}"

    for chat_id in admin_ids:
        try:
            requests.post(f"{base}/sendMessage", data={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown',
            }, timeout=10)

            if ariza.education_diploma:
                with open(ariza.education_diploma.path, 'rb') as f:
                    requests.post(f"{base}/sendDocument", files={'document': f}, data={
                        'chat_id': chat_id,
                        'caption': f"Ta'lim diplomi — {ariza.full_name}",
                    }, timeout=30)

            for afile in ariza.files.all():
                try:
                    with open(afile.file.path, 'rb') as f:
                        requests.post(f"{base}/sendDocument", files={'document': f}, data={
                            'chat_id': chat_id,
                            'caption': f"{afile.get_file_type_display()} — {ariza.full_name}",
                        }, timeout=30)
                except Exception:
                    pass
        except Exception:
            pass


def _send_email(ariza):
    notification_email = getattr(settings, 'NOTIFICATION_EMAIL', None)
    if not notification_email:
        return

    millat = ariza.get_nationality_display()
    if ariza.nationality == 'other' and ariza.nationality_other:
        millat = ariza.nationality_other

    body = f"""Yangi ish o'rni arizasi keldi!

F.I.Sh:          {ariza.full_name}
Telefon:         {ariza.phone}
Email:           {ariza.email}
Millat:          {millat}
Yashash manzili: {ariza.address}
Tug'ilgan sana:  {ariza.birth_date.strftime('%d.%m.%Y')}
Ma'lumot:        {ariza.get_education_level_display()}
Ta'lim muassasasi: {ariza.institution}
Ilmiy unvon:     {ariza.academic_title or '—'}
Ilmiy daraja:    {ariza.academic_degree or '—'}
Xorijiy til:     {ariza.foreign_language or '—'}

Yuborilgan vaqt: {ariza.created_at.strftime('%d.%m.%Y %H:%M')}

Admin panelda ko'rish: https://qabul.samduuf.uz/admin/employees/ishariza/{ariza.pk}/change/
"""
    try:
        email = EmailMessage(
            subject=f"Yangi ariza: {ariza.full_name}",
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[notification_email],
        )
        # Asosiy diplom
        if ariza.education_diploma:
            email.attach_file(ariza.education_diploma.path)
        # Qo'shimcha fayllar
        for afile in ariza.files.all():
            try:
                email.attach_file(afile.file.path)
            except Exception:
                pass
        email.send(fail_silently=True)
    except Exception:
        pass
