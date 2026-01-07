from django.db import models

class TeamMember(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='F.I.SH')
    profession = models.CharField(max_length=150, verbose_name='Lavozimi')
    image = models.ImageField(upload_to='team/', verbose_name='rasm 300 x 300 px ')
    
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Qabul komissiyasi tarkibi "
        verbose_name_plural = "Qabul komissiyasi tarkibi"

    def __str__(self):
        return self.full_name



from django.db import models
from django.core.validators import FileExtensionValidator



class Document(models.Model):
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('DOC', 'DOC/DOCX'),
        ('JPG', 'JPG/JPEG/PNG'),
        ('XLS', 'XLS/XLSX'),
        ('ZIP', 'ZIP/RAR'),
        ('TXT', 'TXT'),
    ]
    
    name = models.CharField(max_length=300, verbose_name="Hujjat nomi")
    description = models.TextField(verbose_name="Hujjat tavsifi")
   
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, 
                                   verbose_name="Fayl formati")
    file = models.FileField(upload_to='documents/%Y/%m/%d/', 
                            validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'xls', 'xlsx', 'zip', 'rar', 'txt'])],
                            verbose_name="Fayl")
    file_size = models.CharField(max_length=50, blank=True, verbose_name="Fayl hajmi")
    download_count = models.IntegerField(default=0, verbose_name="Yuklab olishlar soni")
    view_count = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file:
            # Fayl hajmini hisoblash
            size = self.file.size
            if size < 1024:
                self.file_size = f"{size} B"
            elif size < 1024 * 1024:
                self.file_size = f"{size / 1024:.1f} KB"
            else:
                self.file_size = f"{size / (1024 * 1024):.1f} MB"
        super().save(*args, **kwargs)

    def get_file_extension(self):
        return self.file.name.split('.')[-1].upper()

    def get_download_url(self):
        return self.file.url if self.file else "#"

class ImportantNote(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Mazmuni")
    icon = models.CharField(max_length=100, default="fas fa-exclamation-circle", verbose_name="Ikonka")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Muhim eslatma"
        verbose_name_plural = "Muhim eslatmalar"
        ordering = ['order']

    def __str__(self):
        return self.title

class AdmissionRule(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Mazmuni")
    rule_type = models.CharField(max_length=50, choices=[
        ('bakalavr', 'Bakalavriat'),
        ('magistr', 'Magistratura'),
        ('step', 'Bosqich'),
        ('general', 'Umumiy'),
    ], default='general', verbose_name="Qoida turi")
    icon = models.CharField(max_length=100, default="fas fa-graduation-cap", verbose_name="Ikonka")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Qabul qoidasi"
        verbose_name_plural = "Qabul qoidalari"
        ordering = ['order']

    def __str__(self):
        return self.title

class Deadline(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi")
    description = models.TextField(verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Muddat"
        verbose_name_plural = "Muddatlar"
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

    def is_current(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
    



    #qabul kuni

    from django.db import models

class QabulJadvali(models.Model):
    KUNLAR = [
        ('Dushanba', 'Dushanba'),
        ('Seshanba', 'Seshanba'),
        ('Chorshanba', 'Chorshanba'),
        ('Payshanba', 'Payshanba'),
        ('Juma', 'Juma'),
        ('Shanba', 'Shanba'),
    ]

    lavozim = models.CharField(max_length=100)
    fish = models.CharField("F.I.Sh", max_length=150)
    telefon = models.CharField("Telefon raqami", max_length=20)
    qabul_kuni = models.CharField(max_length=20, choices=KUNLAR)
    vaqt = models.CharField(max_length=50)
    xona = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.lavozim} – {self.fish}"

    class Meta:
        verbose_name = "Qabul jadvali"
        verbose_name_plural = "Qabul jadvallari"
