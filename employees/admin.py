from django.contrib import admin
from .models import QabulKomissiya

@admin.register(QabulKomissiya)
class QabulKomissiyaAdmin(admin.ModelAdmin):
    list_display = (
        'familiya',
        'ism',
        'lavozim',
        'lavozim_turi',
        'telefon',
        'is_active',
        'tartib'
    )

    list_filter = ('lavozim_turi', 'is_active')
    search_fields = ('ism', 'familiya', 'lavozim')
    list_editable = ('is_active', 'tartib')
    ordering = ('tartib',)
