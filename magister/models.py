from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class QabulRijasi(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Qabul Rijasi sahifasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "QabulRijasi"
        verbose_name_plural = "QabulRijasi"

    def __str__(self):
        return self.title
    


class MagistraturaNatijalari(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Magistratura natijalari sahifasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Magistratura"
        verbose_name_plural = "Magistratura"

    def __str__(self):
        return self.title


