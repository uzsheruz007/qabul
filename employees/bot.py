import json
import os
import re
import requests
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile

TOKEN   = settings.TELEGRAM_BOT_TOKEN
API     = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"

# ── helpers ──────────────────────────────────────────────────────────────────

def _post(method, **kwargs):
    try:
        requests.post(f"{API}/{method}", timeout=10, **kwargs)
    except Exception:
        pass


def send(chat_id, text, markup=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if markup:
        payload['reply_markup'] = json.dumps(markup)
    _post('sendMessage', data=payload)


def answer_cb(cb_id):
    _post('answerCallbackQuery', data={'callback_query_id': cb_id})


def inline(*rows):
    return {'inline_keyboard': list(rows)}


def btn(label, cb):
    return {'text': label, 'callback_data': cb}


NAT_KB = inline(
    [btn("O'zbek", 'nat:uzbek'), btn("Boshqa", 'nat:other')]
)

EDU_KB = inline(
    [btn("O'rta", 'edu:urta'), btn("O'rta maxsus", 'edu:urta_maxsus')],
    [btn("Oliy — bakalavr", 'edu:oliy_bakalavr')],
    [btn("Oliy — magistr",  'edu:oliy_magistr')],
    [btn("Oliy — doktorant/PhD", 'edu:oliy_doktorant')],
)

EDU_LABELS = {
    'urta':           "O'rta",
    'urta_maxsus':    "O'rta maxsus / kasb-hunar",
    'oliy_bakalavr':  "Oliy (bakalavr)",
    'oliy_magistr':   "Oliy (magistr)",
    'oliy_doktorant': "Oliy (doktorant/PhD)",
}

PROMPTS = {
    'full_name':           "👤 <b>1/9 · F.I.Sh ni kiriting:</b>\n<i>Masalan: Usmonov Erkin Baxtiyorovich</i>",
    'phone':               "📞 <b>2/9 · Telefon raqamingiz:</b>\n<i>Masalan: +998901234567</i>",
    'email':               "📧 <b>3/9 · Email manzilingiz:</b>",
    'nationality':         "🌍 <b>4/9 · Millatingizni tanlang:</b>",
    'address':             "🏠 <b>5/9 · Yashash manzilingiz:</b>\n<i>Viloyat, tuman, ko'cha, uy raqami</i>",
    'birth_date':          "🎂 <b>6/9 · Tug'ilgan sanangiz:</b>\n<i>Format: KK.OO.YYYY — masalan 15.06.1990</i>",
    'education_level':     "🎓 <b>7/9 · Ma'lumotingizni tanlang:</b>",
    'institution':         "🏛 <b>8/9 · Ta'lim muassasasi nomi:</b>",
    'education_diploma':   "📄 <b>9/9 · Ta'lim diplomi faylini yuboring</b>\n<i>PDF, JPG yoki PNG · maks 10 MB</i>",
    'academic_title':      "🏅 <b>Ilmiy unvoningiz</b> (ixtiyoriy):\n<i>Masalan: Dotsent</i>\n👉 /skip — o'tkazib yuborish",
    'academic_title_file': "📎 <b>Ilmiy unvon diplomi</b> faylini yuboring\n👉 /skip — o'tkazib yuborish",
    'academic_degree':     "🔬 <b>Ilmiy darajangiz</b> (ixtiyoriy):\n<i>Masalan: Falsafa doktori (PhD)</i>\n👉 /skip — o'tkazib yuborish",
    'academic_degree_file':"📎 <b>Ilmiy daraja diplomi</b> faylini yuboring\n👉 /skip — o'tkazib yuborish",
    'foreign_language':    "🌐 <b>Xorijiy til bilish darajasi</b> (ixtiyoriy):\n<i>Masalan: Ingliz tili — B2 (IELTS 6.0)</i>\n👉 /skip — o'tkazib yuborish",
    'language_cert_file':  "📎 <b>Til sertifikati</b> faylini yuboring\n👉 /skip — o'tkazib yuborish",
    'work_reference_file': "📁 <b>Mehnat faoliyati ma'lumotnomasi</b> (ixtiyoriy):\n<i>Avvalgi ish joyi ma'lumotnomasi</i>\n👉 /skip — o'tkazib yuborish",
}

FILE_STEPS = {
    'education_diploma',
    'academic_title_file',
    'academic_degree_file',
    'language_cert_file',
    'work_reference_file',
}

# ── main entry point ─────────────────────────────────────────────────────────

def handle_update(update):
    if 'callback_query' in update:
        _handle_callback(update['callback_query'])
    elif 'message' in update:
        _handle_message(update['message'])


# ── callback (inline keyboard) ───────────────────────────────────────────────

def _handle_callback(cq):
    from .models import BotSession
    chat_id = str(cq['message']['chat']['id'])
    data    = cq['data']
    answer_cb(cq['id'])

    session, _ = BotSession.objects.get_or_create(chat_id=chat_id)

    if data.startswith('nat:') and session.step == 'nationality':
        val = data.split(':', 1)[1]
        session.data['nationality'] = val
        if val == 'other':
            session.step = 'nationality_other'
            session.save()
            send(chat_id, "🌍 Millatingizni yozing:")
        else:
            session.step = 'address'
            session.save()
            send(chat_id, PROMPTS['address'])

    elif data.startswith('edu:') and session.step == 'education_level':
        val = data.split(':', 1)[1]
        session.data['education_level'] = val
        session.step = 'institution'
        session.save()
        send(chat_id, PROMPTS['institution'])


# ── message ──────────────────────────────────────────────────────────────────

def _handle_message(message):
    from .models import BotSession
    chat_id  = str(message['chat']['id'])
    text     = message.get('text', '').strip()
    doc      = (message.get('document') or
                (message.get('photo') and message['photo'][-1]))

    session, _ = BotSession.objects.get_or_create(chat_id=chat_id)

    # ── commands ──
    if text == '/start':
        session.step = 'full_name'
        session.data = {}
        session.save()
        send(chat_id,
             "👋 <b>Salom! SamDU Urgut filiali — Ish o'rinlari boti</b>\n\n"
             "Bu bot orqali bo'sh ish o'rinlari uchun hujjat topshirishingiz mumkin.\n\n"
             "▶️ Ariza boshlash: /ariza\n"
             "❌ Bekor qilish: /cancel")
        return

    if text == '/ariza':
        session.step = 'full_name'
        session.data = {}
        session.save()
        send(chat_id, "📋 <b>Ariza boshlandi!</b>\nSavollarga ketma-ket javob bering.\n"
                      "Istalgan vaqt bekor qilish: /cancel\n\n" + PROMPTS['full_name'])
        return

    if text == '/cancel':
        session.step = 'full_name'
        session.data = {}
        session.save()
        send(chat_id, "❌ Ariza bekor qilindi.\n▶️ Qayta boshlash: /ariza")
        return

    step = session.step

    # ── file steps ──
    if step in FILE_STEPS:
        is_skip = (text == '/skip' and step != 'education_diploma')

        if is_skip:
            _advance_from_file_step(chat_id, session, step, skipped=True)
            return

        if not doc:
            send(chat_id, "⚠️ Iltimos, <b>fayl yuboring</b> (PDF, JPG, PNG)."
                          + ("\n👉 /skip — o'tkazib yuborish" if step != 'education_diploma' else ""))
            return

        fid   = doc.get('file_id')
        fname = doc.get('file_name', 'fayl.pdf')

        if step == 'education_diploma':
            session.data['education_diploma_file_id']   = fid
            session.data['education_diploma_filename']  = fname
        elif step == 'academic_title_file':
            session.data.setdefault('academic_title_file_ids', []).append(fid)
        elif step == 'academic_degree_file':
            session.data.setdefault('academic_degree_file_ids', []).append(fid)
        elif step == 'language_cert_file':
            session.data.setdefault('language_cert_file_ids', []).append(fid)
        elif step == 'work_reference_file':
            session.data.setdefault('work_reference_file_ids', []).append(fid)

        session.save()
        _advance_from_file_step(chat_id, session, step, skipped=False)
        return

    # ── text steps ──
    if not text:
        return

    if step == 'full_name':
        session.data['full_name'] = text
        session.step = 'phone'
        session.save()
        send(chat_id, PROMPTS['phone'])

    elif step == 'phone':
        if not re.match(r'^\+?[\d\s\-]{7,20}$', text):
            send(chat_id, "⚠️ Telefon raqamni to'g'ri kiriting.\n<i>Masalan: +998901234567</i>")
            return
        session.data['phone'] = text
        session.step = 'email'
        session.save()
        send(chat_id, PROMPTS['email'])

    elif step == 'email':
        if '@' not in text or '.' not in text.split('@')[-1]:
            send(chat_id, "⚠️ Email manzilni to'g'ri kiriting.\n<i>Masalan: ism@gmail.com</i>")
            return
        session.data['email'] = text
        session.step = 'nationality'
        session.save()
        send(chat_id, PROMPTS['nationality'], NAT_KB)

    elif step == 'nationality_other':
        session.data['nationality_other'] = text
        session.step = 'address'
        session.save()
        send(chat_id, PROMPTS['address'])

    elif step == 'address':
        session.data['address'] = text
        session.step = 'birth_date'
        session.save()
        send(chat_id, PROMPTS['birth_date'])

    elif step == 'birth_date':
        try:
            dt = datetime.strptime(text, '%d.%m.%Y')
            session.data['birth_date'] = dt.strftime('%Y-%m-%d')
        except ValueError:
            send(chat_id, "⚠️ Sana formatini to'g'ri kiriting.\n<i>Masalan: 15.06.1990</i>")
            return
        session.step = 'education_level'
        session.save()
        send(chat_id, PROMPTS['education_level'], EDU_KB)

    elif step == 'institution':
        session.data['institution'] = text
        session.step = 'education_diploma'
        session.save()
        send(chat_id, PROMPTS['education_diploma'])

    elif step == 'academic_title':
        if text == '/skip':
            session.data['academic_title'] = ''
            session.step = 'academic_degree'
        else:
            session.data['academic_title'] = text
            session.step = 'academic_title_file'
        session.save()
        send(chat_id, PROMPTS[session.step])

    elif step == 'academic_degree':
        if text == '/skip':
            session.data['academic_degree'] = ''
            session.step = 'foreign_language'
        else:
            session.data['academic_degree'] = text
            session.step = 'academic_degree_file'
        session.save()
        send(chat_id, PROMPTS[session.step])

    elif step == 'foreign_language':
        if text == '/skip':
            session.data['foreign_language'] = ''
            session.step = 'work_reference_file'
        else:
            session.data['foreign_language'] = text
            session.step = 'language_cert_file'
        session.save()
        send(chat_id, PROMPTS[session.step])

    else:
        send(chat_id, "▶️ Boshlash uchun /ariza yuboring.")


# ── file step transitions ─────────────────────────────────────────────────────

def _advance_from_file_step(chat_id, session, step, skipped):
    next_map = {
        'education_diploma':    'academic_title',
        'academic_title_file':  'academic_degree',
        'academic_degree_file': 'foreign_language',
        'language_cert_file':   'work_reference_file',
        'work_reference_file':  'done',
    }
    nxt = next_map[step]
    if nxt == 'done':
        session.step = 'full_name'
        session.data_snapshot = dict(session.data)
        data_copy = dict(session.data)
        session.data = {}
        session.save()
        _finalize(chat_id, data_copy)
    else:
        session.step = nxt
        session.save()
        send(chat_id, PROMPTS[nxt])


# ── finalize: save to DB + notify ────────────────────────────────────────────

def _finalize(chat_id, d):
    from .models import IshAriza, IshArizaFile
    from .views import _send_telegram, _send_email

    ariza = IshAriza(
        full_name       = d.get('full_name', ''),
        phone           = d.get('phone', ''),
        email           = d.get('email', ''),
        nationality     = d.get('nationality', 'uzbek'),
        nationality_other = d.get('nationality_other', ''),
        address         = d.get('address', ''),
        birth_date      = d.get('birth_date'),
        education_level = d.get('education_level', 'oliy_bakalavr'),
        institution     = d.get('institution', ''),
        academic_title  = d.get('academic_title', ''),
        academic_degree = d.get('academic_degree', ''),
        foreign_language= d.get('foreign_language', ''),
    )

    # Download main diploma
    fid   = d.get('education_diploma_file_id')
    fname = d.get('education_diploma_filename', 'diplom.pdf')
    if fid:
        content, real_name = _download(fid)
        if content:
            ariza.education_diploma.save(real_name or fname, ContentFile(content), save=False)

    ariza.save()

    # Additional files
    _save_files(ariza, d.get('academic_title_file_ids', []),   'academic_title')
    _save_files(ariza, d.get('academic_degree_file_ids', []),  'academic_degree')
    _save_files(ariza, d.get('language_cert_file_ids', []),    'language_cert')
    _save_files(ariza, d.get('work_reference_file_ids', []),   'work_reference')

    # Notify admin (Telegram + Email)
    _send_telegram(ariza)
    _send_email(ariza)

    # Confirm to user
    send(chat_id,
         "✅ <b>Arizangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
         f"<b>Ism:</b> {ariza.full_name}\n"
         f"<b>Telefon:</b> {ariza.phone}\n\n"
         "📞 Tez orada siz bilan bog'lanamiz.\n"
         "❓ Savol: <b>+998 93 333 20 14</b>")


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
    except Exception:
        return None, None
