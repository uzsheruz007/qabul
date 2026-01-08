from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class ForeignStudentRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('answered', 'Javob berildi'),
    )

    full_name = models.CharField(max_length=255, verbose_name="F.I.Sh")
    country = models.CharField(max_length=100, verbose_name="Davlat")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=30, verbose_name="Telefon raqam")
    faculty = models.CharField(max_length=150, verbose_name="Qiziqqan yo‘nalish")
    message = models.TextField(verbose_name="Murojaat matni")

    admin_reply = models.TextField(
        blank=True,
        null=True,
        verbose_name="Qabul bo‘limi javobi"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Xorijiy talaba murojaati"
        verbose_name_plural = "Xorijiy talabalar murojaatlari"



class Bakalaver(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Bakalaver sahifasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bakalaver"
        verbose_name_plural = "Bakalaver"

    def __str__(self):
        return self.title
    


class Magistratura(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Magistratura sahifasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Magistratura"
        verbose_name_plural = "Magistratura"

    def __str__(self):
        return self.title



class Shartnomalar(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Shartnomalar sahifasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shartnomalar"
        verbose_name_plural = "Shartnomalar"

    def __str__(self):
        return self.title



class Kontrakt(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Kontrakt sahifasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kontrakt"
        verbose_name_plural = "Kontrakt"

    def __str__(self):
        return self.title