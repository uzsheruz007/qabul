from django.db import models


class IshAriza(models.Model):
    MILLAT_CHOICES = [
        ('uzbek', "O'zbek"),
        ('other', 'Boshqa'),
    ]
    MALUMOT_CHOICES = [
        ('urta', "O'rta"),
        ('urta_maxsus', "O'rta maxsus / kasb-hunar"),
        ('oliy_bakalavr', 'Oliy (bakalavr)'),
        ('oliy_magistr', 'Oliy (magistr)'),
        ('oliy_doktorant', 'Oliy (doktorant / PhD)'),
    ]
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('reviewing', "Ko'rib chiqilmoqda"),
        ('approved', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    ]

    full_name        = models.CharField(max_length=200, verbose_name="F.I.Sh")
    phone            = models.CharField(max_length=20, default='', verbose_name="Telefon raqam")
    email            = models.EmailField(default='', verbose_name="Email manzil")
    nationality      = models.CharField(max_length=20, choices=MILLAT_CHOICES, verbose_name="Millat")
    nationality_other = models.CharField(max_length=100, blank=True, verbose_name="Boshqa millat")
    address          = models.CharField(max_length=300, verbose_name="Yashash manzili")
    birth_date       = models.DateField(verbose_name="Tug'ilgan sana")
    education_level  = models.CharField(max_length=30, choices=MALUMOT_CHOICES, verbose_name="Ma'lumot")
    education_diploma = models.FileField(upload_to='ish_ariza/diplom/', verbose_name="Ta'lim diplomi")
    academic_title   = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy unvon")
    academic_degree  = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy daraja")
    foreign_language = models.CharField(max_length=200, blank=True, verbose_name="Xorijiy til darajasi")
    institution      = models.CharField(max_length=300, verbose_name="Ta'lim muassasasi")
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holat")
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ish o'rni arizasi"
        verbose_name_plural = "Ish o'rni arizalari"

    def __str__(self):
        return f"{self.full_name} — {self.created_at.strftime('%d.%m.%Y')}"


class BotSession(models.Model):
    chat_id    = models.CharField(max_length=50, unique=True)
    step       = models.CharField(max_length=50, default='full_name')
    data       = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bot sessiyasi"
        verbose_name_plural = "Bot sessiyalari"

    def __str__(self):
        return f"Chat {self.chat_id} → {self.step}"


class IshArizaFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('academic_title',  'Ilmiy unvon diplomi'),
        ('academic_degree', 'Ilmiy daraja diplomi'),
        ('language_cert',   'Til sertifikati'),
        ('work_reference',  "Mehnat faoliyati ma'lumotnomasi"),
    ]

    ariza     = models.ForeignKey(IshAriza, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=30, choices=FILE_TYPE_CHOICES)
    file      = models.FileField(upload_to='ish_ariza/files/')

    class Meta:
        verbose_name = "Ariza fayli"
        verbose_name_plural = "Ariza fayllari"

    def __str__(self):
        return f"{self.ariza.full_name} — {self.get_file_type_display()}"


class QabulKomissiya(models.Model):
    LAVOZIM_TURI = (
        ('rais', 'Komissiya raisi'),
        ('kotib', 'Mas’ul kotib'),
        ('azo', 'Komissiya a’zosi'),
        ('rahbar', 'Guruh rahbari'),
    )

    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    lavozim = models.CharField(max_length=200)
    lavozim_turi = models.CharField(
        max_length=20,
        choices=LAVOZIM_TURI,
        default='azo'
    )

    email = models.EmailField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    rasm = models.ImageField(upload_to='komissiya/', blank=True, null=True)

    tartib = models.PositiveIntegerField(
        default=0,
        help_text="Ekranda chiqish tartibi"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['tartib']
        verbose_name = "Qabul komissiya a’zosi"
        verbose_name_plural = "Qabul komissiya a’zolari"

    def __str__(self):
        return f"{self.familiya} {self.ism} ({self.lavozim})"
