from django.contrib import admin
from .models import QabulRijasi, MagistraturaNatijalari
# Register your models here.

@admin.register(QabulRijasi)
class QabulRijasiAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(MagistraturaNatijalari)
class MagistraturaNatijalariAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')