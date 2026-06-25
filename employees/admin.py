from django.contrib import admin
from .models import QabulKomissiya, IshAriza, IshArizaFile

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


class IshArizaFileInline(admin.TabularInline):
    model = IshArizaFile
    extra = 0
    readonly_fields = ('file_type', 'file')


@admin.register(IshAriza)
class IshArizaAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'nationality', 'education_level', 'institution', 'status', 'created_at')
    list_filter   = ('status', 'nationality', 'education_level')
    search_fields = ('full_name', 'address', 'institution')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    inlines = [IshArizaFileInline]
