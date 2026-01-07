from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profession', 'created_at')
    search_fields = ('full_name', 'profession')
    list_filter = ('created_at',)




from django.contrib import admin
from django.utils.html import format_html
from .models import  Document, ImportantNote, AdmissionRule, Deadline


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name',  'file_format', 'file_size', 'download_count', 'view_count', 'is_active']
    list_filter = [ 'file_format', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['download_count', 'view_count', 'file_size', 'created_at', 'updated_at']
    ordering = ['order', 'name']
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('name', 'description',  'file_format', 'file', 'order', 'is_active')
        }),
        ('Statistika', {
            'fields': ('download_count', 'view_count', 'file_size')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'file' in form.changed_data:
            # Yangi fayl yuklangan
            obj.download_count = 0
            obj.view_count = 0
        super().save_model(request, obj, form, change)

@admin.register(ImportantNote)
class ImportantNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']
    ordering = ['order']

@admin.register(AdmissionRule)
class AdmissionRuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'rule_type', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['rule_type', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']
    ordering = ['order']

@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active', 'is_current']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    ordering = ['-start_date']
    
    def is_current(self, obj):
        return obj.is_current()
    is_current.boolean = True
    is_current.short_description = "Joriy muddat"






    from django.contrib import admin
from .models import QabulJadvali

@admin.register(QabulJadvali)
class QabulJadvaliAdmin(admin.ModelAdmin):
    list_display = ('lavozim', 'fish', 'telefon', 'qabul_kuni', 'vaqt', 'xona')
    list_filter = ('qabul_kuni',)
    search_fields = ('fish', 'lavozim', 'telefon')
    ordering = ('qabul_kuni',)
