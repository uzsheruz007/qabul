from django.db import models
from django.utils import timezone
import os

def passport_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'passport_{instance.full_name.replace(" ", "_")}_{instance.id}.{ext}'
    return os.path.join('passports', filename)

def diploma_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'diploma_{instance.full_name.replace(" ", "_")}_{instance.id}.{ext}'
    return os.path.join('diplomas', filename)

class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Mamlakat nomi")
    code = models.CharField(max_length=10, verbose_name="Mamlakat kodi")
    
    class Meta:
        verbose_name = "Mamlakat"
        verbose_name_plural = "Mamlakatlar"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class StudyProgram(models.Model):
    PROGRAM_TYPES = [
        ('bachelor', "Bakalavr"),
        ('master', "Magistr"),
        ('phd', "PhD"),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Dastur nomi")
    code = models.CharField(max_length=50, verbose_name="Dastur kodi")
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES, verbose_name="Dastur turi")
    duration = models.IntegerField(verbose_name="O'qish muddati (yil)")
    description = models.TextField(verbose_name="Tavsif", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        verbose_name = "O'quv dasturi"
        verbose_name_plural = "O'quv dasturlari"
        ordering = ['program_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_program_type_display()})"

class Application(models.Model):
    APPLICATION_STATUS = [
        ('new', "Yangi"),
        ('reviewed', "Ko'rib chiqilgan"),
        ('accepted', "Qabul qilingan"),
        ('rejected', "Rad etilgan"),
        ('waiting', "Kutish ro'yxatida"),
    ]
    
    GENDER_CHOICES = [
        ('male', "Erkak"),
        ('female', "Ayol"),
    ]
    
    # Shaxsiy ma'lumotlar
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    date_of_birth = models.DateField(verbose_name="Tug'ilgan sana")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Jinsi")
    nationality = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='applications', verbose_name="Fuqarolik")
    passport_number = models.CharField(max_length=50, verbose_name="Passport raqami")
    passport_issue_date = models.DateField(verbose_name="Passport berilgan sana")
    passport_expiry_date = models.DateField(verbose_name="Passport amal qilish muddati")
    passport_photo = models.ImageField(upload_to=passport_upload_path, verbose_name="Passport nusxasi")
    
    # Aloqa ma'lumotlari
    email = models.EmailField(verbose_name="Elektron pochta")
    phone = models.CharField(max_length=50, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Yashash manzili")
    city = models.CharField(max_length=100, verbose_name="Shahar")
    postal_code = models.CharField(max_length=20, verbose_name="Pochta indeksi", blank=True)
    
    # O'qish ma'lumotlari
    study_program = models.ForeignKey(StudyProgram, on_delete=models.PROTECT, verbose_name="O'quv dasturi")
    previous_education = models.CharField(max_length=200, verbose_name="Oldingi ta'lim")
    previous_institution = models.CharField(max_length=300, verbose_name="Oldingi o'quv muassasasi")
    graduation_year = models.IntegerField(verbose_name="Bitirgan yili")
    gpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="O'rtacha baho (GPA)")
    diploma_copy = models.ImageField(upload_to=diploma_upload_path, verbose_name="Diplom nusxasi")
    
    # Qo'shimcha ma'lumotlar
    motivation_letter = models.TextField(verbose_name="Motivatsion xat")
    emergency_contact_name = models.CharField(max_length=200, verbose_name="Favqulodda vaziyatdagi aloqa shaxsi")
    emergency_contact_phone = models.CharField(max_length=50, verbose_name="Favqulodda aloqa telefon raqami")
    
    # Tizim ma'lumotlari
    application_date = models.DateTimeField(default=timezone.now, verbose_name="Ariza sanasi")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='new', verbose_name="Holati")
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    
    # Elektron pochta yuborish
    confirmation_sent = models.BooleanField(default=False, verbose_name="Tasdiqlash xabari yuborilgan")
    admin_notified = models.BooleanField(default=False, verbose_name="Administratorga xabar berilgan")
    
    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.full_name} - {self.study_program.name}"
    
    def get_age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))