from django.db import models
from django.utils.text import slugify


class PrivilegeCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(
        max_length=10,
        help_text="Emoji yoki icon (👨‍👩‍👧‍👦)",
        verbose_name="Icon"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Imtiyoz kategoriyasi"
        verbose_name_plural = "Imtiyoz kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Privilege(models.Model):
    category = models.ForeignKey(
        PrivilegeCategory,
        on_delete=models.CASCADE,
        related_name="privileges",
        verbose_name="Kategoriya"
    )
    title = models.CharField(max_length=255, verbose_name="Imtiyoz nomi")
    description = models.TextField(verbose_name="Tavsif")
    documents = models.TextField(
        verbose_name="Kerakli hujjatlar",
        help_text="Har bir hujjatni yangi qatordan yozing"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Imtiyoz"
        verbose_name_plural = "Imtiyozlar"

    def document_list(self):
        return self.documents.splitlines()

    def __str__(self):
        return self.title


from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class QabulKvotasi(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    content = CKEditor5Field(
        'Qabul kvotasi matni',
        config_name='default'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Qabul kvotasi"
        verbose_name_plural = "Qabul kvotasi"

    def __str__(self):
        return self.title
