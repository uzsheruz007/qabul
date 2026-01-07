from django.db import models

class QabulKomissiya(models.Model):
    LAVOZIM_TURI = (
        ('rais', 'Komissiya raisi'),
        ('kotib', 'Mas’ul kotib'),
        ('azo', 'Komissiya a’zosi'),
        ('rahbar', 'Guruh rahbari'),
    )

    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    lavozim = models.CharField(max_length=50)
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
