from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import ForeignStudentRequest, Bakalaver, Shartnomalar, Kontrakt

@admin.register(ForeignStudentRequest)
class ForeignStudentRequestAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'country',
        'email',
        'faculty',
        'status',
        'created_at'
    )

    list_filter = ('status', 'country')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Talaba ma’lumotlari", {
            'fields': (
                'full_name',
                'country',
                'email',
                'phone',
                'faculty',
                'message',
                'created_at'
            )
        }),
        ("Qabul bo‘limi javobi", {
            'fields': ('admin_reply', 'status')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and obj.status != 'answered':
            send_mail(
                subject="Qabul bo‘limidan javob",
                message=obj.admin_reply,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
                fail_silently=False
            )
            obj.status = 'answered'

        super().save_model(request, obj, form, change)



@admin.register(Bakalaver)
class BakalaverAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Shartnomalar)
class ShartnomalarAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Kontrakt)
class KontraktAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')