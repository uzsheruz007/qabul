import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings

def send_application_email(application):
    """Ariza muvaffaqiyatli yuborilganda elektron pochta yuborish"""
    
    # Talabaga tasdiqlash xabari
    subject = f"Bilasan Universiteti - Ariza qabul qilindi #{application.id}"
    context = {
        'application': application,
        'date': timezone.now().date(),
    }
    
    html_message = render_to_string('xorijiy/email/application_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[application.email],
        reply_to=[settings.ADMIN_EMAIL],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
    
    # Administratorga xabar
    admin_subject = f"Yangi talaba arizasi: {application.full_name}"
    admin_html_message = render_to_string('xorijiy/email/new_application_notification.html', context)
    admin_plain_message = strip_tags(admin_html_message)
    
    admin_email = EmailMultiAlternatives(
        subject=admin_subject,
        body=admin_plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )
    admin_email.attach_alternative(admin_html_message, "text/html")
    admin_email.send()

class EmailThread(threading.Thread):
    """Elektron pochta yuborish uchun thread"""
    def __init__(self, application):
        self.application = application
        threading.Thread.__init__(self)
    
    def run(self):
        send_application_email(self.application)