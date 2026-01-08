from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import Application, Country, StudyProgram

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'study_program', 'nationality', 'status', 'application_date_display')
    list_filter = ('status', 'gender', 'study_program', 'nationality', 'application_date')
    search_fields = ('full_name', 'email', 'passport_number', 'phone')
    readonly_fields = ('application_date', 'get_age_display', 'application_link', 'confirmation_sent', 'admin_notified')
    fieldsets = (
        ('Shaxsiy maʼlumotlar', {
            'fields': ('full_name', 'date_of_birth', 'get_age_display', 'gender', 'nationality')
        }),
        ('Passport maʼlumotlari', {
            'fields': ('passport_number', 'passport_issue_date', 'passport_expiry_date', 'passport_photo')
        }),
        ('Aloqa maʼlumotlari', {
            'fields': ('email', 'phone', 'address', 'city', 'postal_code')
        }),
        ('Taʼlim maʼlumotlari', {
            'fields': ('study_program', 'previous_education', 'previous_institution', 
                      'graduation_year', 'gpa', 'diploma_copy')
        }),
        ('Qoʻshimcha maʼlumotlar', {
            'fields': ('motivation_letter', 'emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Ariza maʼlumotlari', {
            'fields': ('application_date', 'status', 'notes', 
                      'confirmation_sent', 'admin_notified', 'application_link')
        }),
    )
    
    actions = ['mark_as_reviewed', 'mark_as_accepted', 'mark_as_rejected', 'send_status_email']
    
    def application_date_display(self, obj):
        return obj.application_date.strftime('%Y-%m-%d %H:%M')
    application_date_display.short_description = "Ariza sanasi"
    
    def get_age_display(self, obj):
        return f"{obj.get_age()} yosh"
    get_age_display.short_description = "Yoshi"
    
    def application_link(self, obj):
        url = reverse('application_success', args=[obj.id])
        return format_html(f'<a href="{url}" target="_blank">Arizani ko\'rish</a>')
    application_link.short_description = "Havola"
    
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f"{updated} ta ariza ko'rib chiqilgan holatiga o'tkazildi.")
    mark_as_reviewed.short_description = "Tanlanganlarni ko'rib chiqilgan deb belgilash"
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f"{updated} ta ariza qabul qilingan holatiga o'tkazildi.")
    mark_as_accepted.short_description = "Tanlanganlarni qabul qilingan deb belgilash"
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} ta ariza rad etilgan holatiga o'tkazildi.")
    mark_as_rejected.short_description = "Tanlanganlarni rad etilgan deb belgilash"
    
    def send_status_email(self, request, queryset):
        for application in queryset:
            subject = f"Bilasan Universiteti - Ariza holati yangilandi"
            message = f"Assalomu alaykum {application.full_name},\n\n"
            message += f"Sizning #{application.id} raqamli arizangizning holati yangilandi.\n"
            message += f"Joriy holat: {application.get_status_display()}\n\n"
            message += "Agar qo'shimcha savollaringiz bo'lsa, biz bilan bog'lanishingiz mumkin.\n\n"
            message += "Hurmat bilan,\nBilasan Universiteti Qabul komissiyasi"
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=False,
            )
        
        self.message_user(request, f"{queryset.count()} ta arizaga xabar yuborildi.")
    send_status_email.short_description = "Tanlangan arizalarga holat xabari yuborish"

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class StudyProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'program_type', 'duration', 'is_active')
    list_filter = ('program_type', 'is_active')
    search_fields = ('name', 'code')
    list_editable = ('is_active',)

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(StudyProgram, StudyProgramAdmin)

# Admin panel sozlamalari
admin.site.site_header = "Bilasan Universiteti - Xorijiy Talabalar Qabuli"
admin.site.site_title = "Bilasan Qabul Tizimi"
admin.site.index_title = "Boshqaruv paneli"