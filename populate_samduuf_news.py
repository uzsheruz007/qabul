import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qabul.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
from news.models import Post, Category

User = get_user_model()
main_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

cat_yangiliklar, _ = Category.objects.get_or_create(name="Yangiliklar", defaults={'slug': 'yangiliklar'})
cat_elonlar, _ = Category.objects.get_or_create(name="E'lonlar", defaults={'slug': 'elonlar'})

# Delete dummy posts
Post.objects.all().delete()

news_items = [
    {
        "id": 1,
        "title": "Aniq va tabiiy fanlarda zamonaviy muammolar: ilmiy yondashuvlar va yangi yechimlar mavzusida respublika ilmiy-amaliy konferensiyasi",
        "category": cat_yangiliklar,
        "date": "2026-06-06 10:00:00",
        "image": "blog/images/blog-1.png",
        "content": """SAMARQAND DAVLAT PEDAGOGIKA INSTITUTI URGUT FAKULTETIDa “Aniq va tabiiy fanlarda zamonaviy muammolar: ilmiy yondashuvlar va yangi yechimlar” mavzusidagi respublika miqyosidagi ilmiy-amaliy konferensiya bo'lib o'tdi.

Konferensiyada respublikamizning yetakchi oliy ta'lim muassasalari va ilmiy-tadqiqot institutlaridan taniqli olimlar, professor-o'qituvchilar hamda yosh tadqiqotchilar ishtirok etdilar.

Anjuman davomida matematika, fizika, kimyo va biologiya fanlarining dolzarb masalalari, o'qitish metodikasi va zamonaviy raqamli texnologiyalarni ta'lim jarayoniga tatbiq etish yuzasidan atroflicha fikr almashindi va tegishli ilmiy tavsiyalar ishlab chiqildi."""
    },
    {
        "id": 2,
        "title": "Startap loyihalarni moliyalashtirish va amaliyotga joriy etish masalalariga bagʻishlangan tahliliy yigʻilish",
        "category": cat_yangiliklar,
        "date": "2026-05-26 14:30:00",
        "image": "blog/images/blog-2.png",
        "content": """Urgut fakultetida talaba-yoshlarning innovatsion va startap loyihalarini moliyalashtirish, ularni amaliyotga joriy etish hamda tijoratlashtirish masalalariga bag'ishlangan uchrashuv o'tkazildi.

Yig'ilishda iqtidorli talabalar va yosh olimlar tomonidan tayyorlangan innovatsion ishlanmalar taqdimoti o'tkazildi. Mutaxassislar tomonidan har bir loyihaga amaliy tavsiyalar berildi va ularni moliyalashtirish manbalari muhokama qilindi.

Fakultet rahbariyati iqtidorli yoshlarning g'oya va loyihalarini har tomonlama qo'llab-quvvatlash hamda ilmiy izlanishlar uchun zarur sharoitlarni yaratish borasidagi ishlarni izchil davom ettirishini ta'kidladi."""
    },
    {
        "id": 3,
        "title": "Yoshlar kuni doirasida talabalarning innovatsion gʻoyalari va startap loyihalari saralash bosqichi",
        "category": cat_yangiliklar,
        "date": "2026-05-14 11:00:00",
        "image": "blog/images/blog-4.png",
        "content": """“Yoshlar kuni” munosabati bilan Urgut fakultetida talabalarning innovatsion gʻoyalari va startap proyektlari saralash bosqichi koʻriklari tashkil etildi.

Tadbirda fakultet talabalari o'zlarining axborot texnologiyalari, pedagogika, va tabiiy fanlar sohasidagi eng so'nggi ishlanmalari bilan ishtirok etishdi. 

Hakamlar hay'ati tomonidan eng yaxshi deb topilgan loyihalar respublika va xalqaro tanlovlarga tavsiya etildi hamda g'oliblar qimmatbaho esdalik sovg'alari bilan taqdirlandilar."""
    },
    {
        "id": 4,
        "title": "Tambov davlat universiteti bilan hamkorlikda Rus tili — doʻstligimiz tili xalqaro talabalar olimpiadasi",
        "category": cat_yangiliklar,
        "date": "2026-05-12 15:00:00",
        "image": "blog/images/carousel-2.png",
        "content": """Tambov davlat universiteti hamda Urgut fakulteti hamkorligida “Rus tili — doʻstligimiz tili” mavzusida xalqaro talabalar olimpiadasi muvaffaqiyatli o'tkazildi.

Olimpiadada rus tili va adabiyoti yo'nalishi talabalari til bilish darajasi, adabiy tahlil va muloqot madaniyati bo'yicha o'z bilimlarini namoyish etishdi. 

Xalqaro hamkorlik doirasida o'tkazilgan ushbu tadbir talabalarning til o'rganishga bo'lgan qiziqishini oshirish hamda xalqaro akademik aloqalarni rivojlantirishga xizmat qiladi."""
    },
    {
        "id": 5,
        "title": "9-may Xotira va qadrlash kuni munosabati bilan ma'naviy-ma'rifiy va xotira tadbiri bo'lib o'tdi",
        "category": cat_yangiliklar,
        "date": "2026-05-09 09:30:00",
        "image": "blog/images/contact-img.png",
        "content": """9-may — Xotira va qadrlash kuni munosabati bilan Urgut fakultetida “Inson aziz — xotira muqaddas” mavzusida ma'naviy-ma'rifiy tadbir va uchrashuv o'tkazildi.

Tadbirda mehnat faxriylari, ustozlar hamda talabalar ishtirok etdilar. Tinch va osuda kunlarimiz uchun kurashgan ajdodlarimiz matonati yod etildi, mehnat veteranlariga hurmat va ehtirom ko'rsatildi.

Talabalar tomonidan tayyorlangan adabiy-badiiy kompozitsiyalar va kuy-qo'shiqlar barchada katta taassurot qoldirdi."""
    },
    {
        "id": 6,
        "title": "Sport kuni doirasida Yurish marafoni va talabalar o'rtasida sport musobaqalari o'tkazildi",
        "category": cat_yangiliklar,
        "date": "2026-05-06 08:00:00",
        "image": "blog/images/instagram-footer-1.jpg",
        "content": """Sog'lom turmush tarzini targ'ib qilish va talabalar o'rtasida jismoniy tarbiya va sportni ommalashtirish maqsadida “Sport kuni” doirasida ommaviy “Yurish marafoni” o'tkazildi.

Marafonda fakultet rahbariyati, professor-o'qituvchilar va yuzlab talaba-yoshlar faol ishtirok etishdi. Shuningdek, futbol, voleybol va shaxmat bo'yicha fakultet birinchiligi musobaqalari bo'lib o'tdi.

Musobaqa g'oliblariga diplom va esdalik sovg'alari topshirildi."""
    },
    {
        "id": 7,
        "title": "OITS, OIV profilaktikasi va sog'lom turmush tarzi mavzusida ma'rifiy davra suhbati",
        "category": cat_elonlar,
        "date": "2026-02-27 14:00:00",
        "image": "blog/images/instagram-footer-2.jpg",
        "content": """Talaba-yoshlar o'rtasida sog'lom turmush tarzini qaror toptirish va yuqumli kasalliklarning oldini olish maqsadida mutaxassis shifokorlar ishtirokida ma'rifiy davra suhbati tashkil etildi.

Tadbirda Tibbiyot xodimlari va mutaxassislar tomonidan OIV/OITS kasalligining kelib chiqishi, profilaktikasi va undan saqlanish yo'llari haqida atrofli ma'lumotlar berildi hamda talabalarning savollariga javob qaytarildi."""
    },
    {
        "id": 8,
        "title": "Xalqaro ona tili kuniga bagʻishlangan ma'naviy-ma'rifiy va adabiy-badiiy kecha",
        "category": cat_yangiliklar,
        "date": "2026-02-21 11:30:00",
        "image": "blog/images/blog-3.png",
        "content": """21-fevral — Xalqaro ona tili kuni munosabati bilan Urgut fakultetida “Ona tilim — g'ururim, iftixorim” nomli ma'naviy-ma'rifiy va adabiy-badiiy kecha o'tkazildi.

Kechada ona tilimizning boy imkoniyatlari, uning tarixiy ildizlari hamda ma'naviyatimizdagi o'rni haqida ma'ruzalar tinglandi. Talabalar ijrosidagi g'azal va sherlar kechaga o'zgacha shukuh bag'ishladi."""
    }
]

for item in news_items:
    dt = datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
    dt_aware = timezone.make_aware(dt)
    
    post = Post.objects.create(
        id=item["id"],
        title=item["title"],
        slug=slugify(item["title"])[:190],
        author=main_user,
        category=item["category"],
        content=item["content"],
        excerpt=item["content"][:280] + "...",
        image=item["image"],
        status='published',
        published_date=dt_aware,
        is_main=(item["id"] == 1)
    )
    print(f"Created post #{post.id}: {post.title[:50]}...")

print(f"\nSUCCESS! Total official 2026 news posts in DB: {Post.objects.count()}")
