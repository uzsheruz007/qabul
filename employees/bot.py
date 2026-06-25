import json
import os
import re
import requests
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile

TOKEN    = settings.TELEGRAM_BOT_TOKEN
API      = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"

EDU_LABELS = {
    'urta':           "O'rta",
    'urta_maxsus':    "O'rta maxsus / kasb-hunar",
    'oliy_bakalavr':  "Oliy (bakalavr)",
    'oliy_magistr':   "Oliy (magistr)",
    'oliy_doktorant': "Oliy (doktorant / PhD)",
}

NAT_LABELS = {
    'uzbek': "O'zbek",
    'other': "Boshqa",
}

# ── pastki darajali yuboruvchi ─────────────────────────────────────────────

def _send(chat_id, text, markup=None):
    payload = {
        'chat_id':    chat_id,
        'text':       text,
        'parse_mode': 'HTML',
    }
    if markup:
        payload['reply_markup'] = json.dumps(markup, ensure_ascii=False)
    try:
        r = requests.post(f"{API}/sendMessage", json=payload, timeout=15)
        return r.json()
    except Exception as e:
        print(f"[BOT] send xatosi: {e}")
        return None


def _kb(*rows):
    """Inline keyboard yaratish."""
    return {'inline_keyboard': [list(row) for row in rows]}


def _btn(text, data):
    return {'text': text, 'callback_data': data}


SKIP_KB = _kb([_btn("O'tkazib yuborish >>", 'skip')])

NAT_KB = _kb(
    [_btn("O'zbek", 'nat:uzbek'), _btn("Boshqa", 'nat:other')]
)

EDU_KB = _kb(
    [_btn("O'rta", 'edu:urta')],
    [_btn("O'rta maxsus / kasb-hunar", 'edu:urta_maxsus')],
    [_btn("Oliy — bakalavr", 'edu:oliy_bakalavr')],
    [_btn("Oliy — magistr",  'edu:oliy_magistr')],
    [_btn("Oliy — doktorant / PhD", 'edu:oliy_doktorant')],
)

# ── savol matni ────────────────────────────────────────────────────────────

def _ask(chat_id, step):
    msgs = {
        'full_name': (
            "👤 <b>1-qadam · F.I.Sh</b>\n"
            "Familiya, ism, sharifingizni to'liq kiriting:\n"
            "<i>Masalan: Usmonov Erkin Baxtiyorovich</i>",
            None
        ),
        'phone': (
            "📞 <b>2-qadam · Telefon raqam</b>\n"
            "<i>Masalan: +998901234567</i>",
            None
        ),
        'email': (
            "📧 <b>3-qadam · Email manzil</b>\n"
            "<i>Masalan: ism@gmail.com</i>",
            None
        ),
        'nationality': (
            "🌍 <b>4-qadam · Millat</b>\n"
            "Quyidagi tugmadan tanlang:",
            NAT_KB
        ),
        'nationality_other': (
            "🌍 Millatingizni yozing:",
            None
        ),
        'address': (
            "🏠 <b>5-qadam · Yashash manzili</b>\n"
            "<i>Viloyat, tuman, ko'cha, uy raqami</i>",
            None
        ),
        'birth_date': (
            "🎂 <b>6-qadam · Tug'ilgan sana</b>\n"
            "<i>Format: KK.OO.YYYY — masalan: 15.06.1990</i>",
            None
        ),
        'education_level': (
            "🎓 <b>7-qadam · Ma'lumot darajasi</b>\n"
            "Quyidagi tugmadan tanlang:",
            EDU_KB
        ),
        'institution': (
            "🏛 <b>8-qadam · Ta'lim muassasasi</b>\n"
            "Olgan ta'lim muassasangiz nomini kiriting:",
            None
        ),
        'education_diploma': (
            "📄 <b>9-qadam · Ta'lim diplomi</b>\n"
            "Diplom faylini yuboring (PDF, JPG, PNG · maks 10 MB):",
            None
        ),
        'academic_title': (
            "🏅 <b>Ilmiy unvon</b> <i>(ixtiyoriy)</i>\n"
            "Ilmiy unvoningiz bo'lsa kiriting:\n"
            "<i>Masalan: Dotsent, Professor</i>",
            SKIP_KB
        ),
        'academic_title_file': (
            "📎 <b>Ilmiy unvon diplomi</b>\n"
            "Diplom faylini yuboring (PDF, JPG, PNG):",
            SKIP_KB
        ),
        'academic_degree': (
            "🔬 <b>Ilmiy daraja</b> <i>(ixtiyoriy)</i>\n"
            "Ilmiy darajangiz bo'lsa kiriting:\n"
            "<i>Masalan: Falsafa doktori (PhD), Fan nomzodi</i>",
            SKIP_KB
        ),
        'academic_degree_file': (
            "📎 <b>Ilmiy daraja diplomi</b>\n"
            "Diplom faylini yuboring (PDF, JPG, PNG):",
            SKIP_KB
        ),
        'foreign_language': (
            "🌐 <b>Xorijiy til</b> <i>(ixtiyoriy)</i>\n"
            "Xorijiy til bilish darajangizni kiriting:\n"
            "<i>Masalan: Ingliz tili — B2 (IELTS 6.0)</i>",
            SKIP_KB
        ),
        'language_cert_file': (
            "📎 <b>Til sertifikati</b>\n"
            "Sertifikat faylini yuboring (PDF, JPG, PNG):",
            SKIP_KB
        ),
        'work_reference_file': (
            "📁 <b>Mehnat faoliyati ma'lumotnomasi</b> <i>(ixtiyoriy)</i>\n"
            "Avvalgi ish joyidan ma'lumotnoma faylini yuboring:",
            SKIP_KB
        ),
    }
    text, markup = msgs.get(step, ("Noma'lum qadam.", None))
    _send(chat_id, text, markup)


# ── asosiy handler ─────────────────────────────────────────────────────────

def handle_update(update):
    try:
        if 'callback_query' in update:
            _handle_callback(update['callback_query'])
        elif 'message' in update:
            _handle_message(update['message'])
    except Exception as e:
        print(f"[BOT] handle_update xatosi: {e}")


# ── callback ───────────────────────────────────────────────────────────────

def _handle_callback(cq):
    from .models import BotSession
    chat_id = str(cq['message']['chat']['id'])
    data    = cq['data']

    # callback spinnerini olib tashlash
    try:
        requests.post(f"{API}/answerCallbackQuery",
                      json={'callback_query_id': cq['id']}, timeout=5)
    except Exception:
        pass

    session, _ = BotSession.objects.get_or_create(chat_id=chat_id)
    step = session.step

    # millat tanlash
    if data.startswith('nat:') and step == 'nationality':
        val = data.split(':', 1)[1]
        session.data['nationality'] = val
        if val == 'other':
            session.step = 'nationality_other'
            session.save()
            _ask(chat_id, 'nationality_other')
        else:
            session.step = 'address'
            session.save()
            _ask(chat_id, 'address')
        return

    # ta'lim darajasi tanlash
    if data.startswith('edu:') and step == 'education_level':
        val = data.split(':', 1)[1]
        session.data['education_level'] = val
        session.step = 'institution'
        session.save()
        _ask(chat_id, 'institution')
        return

    # "Ariza boshlash" tugmasi (/start ekranidan)
    if data == 'start_ariza':
        session.step = 'full_name'
        session.data = {}
        session.save()
        _send(chat_id,
              "<b>Ariza boshlandi!</b>\n"
              "Har bir savolga ketma-ket javob bering.\n"
              "Bekor qilish: /cancel\n"
              "─────────────────")
        _ask(chat_id, 'full_name')
        return

    # "O'tkazib yuborish" tugmasi
    if data == 'skip':
        _handle_skip(chat_id, session)
        return


def _handle_skip(chat_id, session):
    step = session.step
    skip_map = {
        'academic_title':      ('academic_title', '',   'academic_degree'),
        'academic_title_file': (None,             None, 'academic_degree'),
        'academic_degree':     ('academic_degree', '',  'foreign_language'),
        'academic_degree_file':(None,             None, 'foreign_language'),
        'foreign_language':    ('foreign_language', '', 'work_reference_file'),
        'language_cert_file':  (None,             None, 'work_reference_file'),
        'work_reference_file': (None,             None, 'done'),
    }
    if step not in skip_map:
        return
    field, val, nxt = skip_map[step]
    if field:
        session.data[field] = val
    if nxt == 'done':
        data_copy = dict(session.data)
        session.step = 'full_name'
        session.data = {}
        session.save()
        _finalize(chat_id, data_copy)
    else:
        session.step = nxt
        session.save()
        _ask(chat_id, nxt)


# ── xabar ─────────────────────────────────────────────────────────────────

def _handle_message(message):
    from .models import BotSession
    chat_id = str(message['chat']['id'])
    text    = message.get('text', '').strip()
    doc     = (message.get('document') or
               (message.get('photo') and message['photo'][-1]))

    session, _ = BotSession.objects.get_or_create(chat_id=chat_id)

    # buyruqlar
    if text in ('/start', '/ariza', '/cancel'):
        _handle_command(chat_id, text, session)
        return

    step = session.step

    # fayl talab qiluvchi qadamlar
    FILE_STEPS = {
        'education_diploma', 'academic_title_file',
        'academic_degree_file', 'language_cert_file', 'work_reference_file',
    }

    if step in FILE_STEPS:
        if not doc:
            msg = "Iltimos, fayl yuboring (PDF, JPG yoki PNG)."
            if step != 'education_diploma':
                _send(chat_id, msg, SKIP_KB)
            else:
                _send(chat_id, msg)
            return

        fid   = doc.get('file_id')
        fname = doc.get('file_name', 'fayl.pdf')
        _store_file(session, step, fid, fname)
        session.save()
        _next_after_file(chat_id, session, step)
        return

    # matn qadamlar
    if not text:
        return
    _handle_text(chat_id, session, step, text)


def _handle_command(chat_id, cmd, session):
    if cmd == '/start':
        session.step = 'full_name'
        session.data = {}
        session.save()
        _send(chat_id,
              "<b>Salom! SamDU Urgut filiali — Ish o'rinlari boti</b>\n\n"
              "Bu bot orqali bo'sh ish o'rinlari uchun hujjat topshirishingiz mumkin.\n\n"
              "Ariza boshlash uchun /ariza ni yuboring.",
              _kb([_btn("Ariza boshlash", 'start_ariza')]))
    elif cmd == '/ariza':
        session.step = 'full_name'
        session.data = {}
        session.save()
        _send(chat_id,
              "<b>Ariza boshlandi!</b>\n"
              "Har bir savolga ketma-ket javob bering.\n"
              "Bekor qilish: /cancel\n"
              "─────────────────")
        _ask(chat_id, 'full_name')
    elif cmd == '/cancel':
        session.step = 'full_name'
        session.data = {}
        session.save()
        _send(chat_id, "Ariza bekor qilindi.\nQayta boshlash: /ariza")


def _store_file(session, step, fid, fname):
    if step == 'education_diploma':
        session.data['education_diploma_file_id']  = fid
        session.data['education_diploma_filename'] = fname
    elif step == 'academic_title_file':
        session.data.setdefault('academic_title_file_ids', []).append(fid)
    elif step == 'academic_degree_file':
        session.data.setdefault('academic_degree_file_ids', []).append(fid)
    elif step == 'language_cert_file':
        session.data.setdefault('language_cert_file_ids', []).append(fid)
    elif step == 'work_reference_file':
        session.data.setdefault('work_reference_file_ids', []).append(fid)


def _next_after_file(chat_id, session, step):
    next_map = {
        'education_diploma':    'academic_title',
        'academic_title_file':  'academic_degree',
        'academic_degree_file': 'foreign_language',
        'language_cert_file':   'work_reference_file',
        'work_reference_file':  'done',
    }
    nxt = next_map[step]
    if nxt == 'done':
        data_copy = dict(session.data)
        session.step = 'full_name'
        session.data = {}
        session.save()
        _finalize(chat_id, data_copy)
    else:
        session.step = nxt
        session.save()
        _ask(chat_id, nxt)


def _handle_text(chat_id, session, step, text):
    if step == 'full_name':
        session.data['full_name'] = text
        session.step = 'phone'
        session.save()
        _ask(chat_id, 'phone')

    elif step == 'phone':
        if not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', text):
            _send(chat_id, "Telefon raqamni to'g'ri kiriting.\nMasalan: +998901234567")
            return
        session.data['phone'] = text
        session.step = 'email'
        session.save()
        _ask(chat_id, 'email')

    elif step == 'email':
        if '@' not in text or '.' not in text.split('@')[-1]:
            _send(chat_id, "Email manzilni to'g'ri kiriting.\nMasalan: ism@gmail.com")
            return
        session.data['email'] = text
        session.step = 'nationality'
        session.save()
        _ask(chat_id, 'nationality')

    elif step == 'nationality_other':
        session.data['nationality'] = 'other'
        session.data['nationality_other'] = text
        session.step = 'address'
        session.save()
        _ask(chat_id, 'address')

    elif step == 'address':
        session.data['address'] = text
        session.step = 'birth_date'
        session.save()
        _ask(chat_id, 'birth_date')

    elif step == 'birth_date':
        try:
            dt = datetime.strptime(text, '%d.%m.%Y')
            session.data['birth_date'] = dt.strftime('%Y-%m-%d')
        except ValueError:
            _send(chat_id, "Sana formatini to'g'ri kiriting.\nMasalan: 15.06.1990")
            return
        session.step = 'education_level'
        session.save()
        _ask(chat_id, 'education_level')

    elif step == 'institution':
        session.data['institution'] = text
        session.step = 'education_diploma'
        session.save()
        _ask(chat_id, 'education_diploma')

    elif step == 'academic_title':
        session.data['academic_title'] = text
        session.step = 'academic_title_file'
        session.save()
        _ask(chat_id, 'academic_title_file')

    elif step == 'academic_degree':
        session.data['academic_degree'] = text
        session.step = 'academic_degree_file'
        session.save()
        _ask(chat_id, 'academic_degree_file')

    elif step == 'foreign_language':
        session.data['foreign_language'] = text
        session.step = 'language_cert_file'
        session.save()
        _ask(chat_id, 'language_cert_file')

    else:
        _send(chat_id, "Ariza boshlash uchun /ariza yuboring.")


# ── yakunlash ──────────────────────────────────────────────────────────────

def _finalize(chat_id, d):
    from .models import IshAriza, IshArizaFile
    from .views import _send_telegram, _send_email

    # DB ga saqlash
    try:
        nat = d.get('nationality', 'uzbek')
        nat_label = d.get('nationality_other') if nat == 'other' else NAT_LABELS.get(nat, nat)

        ariza = IshAriza(
            full_name        = d.get('full_name', ''),
            phone            = d.get('phone', ''),
            email            = d.get('email', ''),
            nationality      = nat,
            nationality_other= d.get('nationality_other', ''),
            address          = d.get('address', ''),
            birth_date       = d.get('birth_date'),
            education_level  = d.get('education_level', 'oliy_bakalavr'),
            institution      = d.get('institution', ''),
            academic_title   = d.get('academic_title', ''),
            academic_degree  = d.get('academic_degree', ''),
            foreign_language = d.get('foreign_language', ''),
        )

        fid   = d.get('education_diploma_file_id')
        fname = d.get('education_diploma_filename', 'diplom.pdf')
        if fid:
            content, real_name = _download(fid)
            if content:
                ariza.education_diploma.save(real_name or fname, ContentFile(content), save=False)

        ariza.save()

        _save_files(ariza, d.get('academic_title_file_ids', []),  'academic_title')
        _save_files(ariza, d.get('academic_degree_file_ids', []), 'academic_degree')
        _save_files(ariza, d.get('language_cert_file_ids', []),   'language_cert')
        _save_files(ariza, d.get('work_reference_file_ids', []),  'work_reference')

        _send_telegram(ariza)
        _send_email(ariza)

    except Exception as e:
        print(f"[BOT] _finalize xatosi: {e}")
        _send(chat_id, "Xatolik yuz berdi. Iltimos qayta urinib ko'ring: /ariza")
        return

    # Foydalanuvchiga to'liq xulosa
    edu_label = EDU_LABELS.get(d.get('education_level', ''), d.get('education_level', '—'))
    nat_disp  = d.get('nationality_other') if d.get('nationality') == 'other' else NAT_LABELS.get(d.get('nationality', ''), '—')
    birth_fmt = ''
    try:
        birth_fmt = datetime.strptime(d.get('birth_date', ''), '%Y-%m-%d').strftime('%d.%m.%Y')
    except Exception:
        birth_fmt = d.get('birth_date', '—')

    summary = (
        "<b>Arizangiz qabul qilindi!</b>\n"
        "─────────────────────\n"
        f"<b>F.I.Sh:</b> {d.get('full_name', '—')}\n"
        f"<b>Telefon:</b> {d.get('phone', '—')}\n"
        f"<b>Email:</b> {d.get('email', '—')}\n"
        f"<b>Millat:</b> {nat_disp}\n"
        f"<b>Manzil:</b> {d.get('address', '—')}\n"
        f"<b>Tug'ilgan sana:</b> {birth_fmt}\n"
        f"<b>Ma'lumot:</b> {edu_label}\n"
        f"<b>Ta'lim muassasasi:</b> {d.get('institution', '—')}\n"
    )
    if d.get('academic_title'):
        summary += f"<b>Ilmiy unvon:</b> {d['academic_title']}\n"
    if d.get('academic_degree'):
        summary += f"<b>Ilmiy daraja:</b> {d['academic_degree']}\n"
    if d.get('foreign_language'):
        summary += f"<b>Xorijiy til:</b> {d['foreign_language']}\n"
    summary += (
        "─────────────────────\n"
        "Tez orada siz bilan bog'lanamiz!\n"
        "Savol: <b>+998 93 333 20 14</b>"
    )
    _send(chat_id, summary)


def _save_files(ariza, file_ids, file_type):
    from .models import IshArizaFile
    for fid in file_ids:
        content, fname = _download(fid)
        if content:
            af = IshArizaFile(ariza=ariza, file_type=file_type)
            af.file.save(fname or 'file.pdf', ContentFile(content), save=False)
            af.save()


def _download(file_id):
    try:
        r = requests.get(f"{API}/getFile", params={'file_id': file_id}, timeout=10)
        file_path = r.json()['result']['file_path']
        fname = os.path.basename(file_path)
        content = requests.get(f"{FILE_API}/{file_path}", timeout=30).content
        return content, fname
    except Exception as e:
        print(f"[BOT] _download xatosi: {e}")
        return None, None
