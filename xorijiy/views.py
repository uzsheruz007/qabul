from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import Application, StudyProgram
from .forms import ApplicationForm
from .utils import EmailThread

def home2(request):
    programs = StudyProgram.objects.filter(is_active=True)[:6]
    context = {
        'programs': programs,
        'title': "Bilasan Universiteti - Xorijiy Talabalar Qabuli",
    }
    return render(request, 'home.html', context)

def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data.copy()
            cleaned_data.pop('confirm_email', None)
            cleaned_data.pop('agree_terms', None)
            
            application = Application(**cleaned_data)
            application.save()
            
            # Elektron pochta yuborish
            EmailThread(application).start()
            
            application.confirmation_sent = True
            application.admin_notified = True
            application.save()
            
            return redirect('application_success', application_id=application.id)
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'title': "Xorijlik Talabalar Ariza Formasi",
    }
    return render(request, 'application_form.html', context)

def application_success(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    context = {
        'application': application,
        'title': "Arizangiz Qabul Qilindi",
    }
    return render(request, 'application_success.html', context)

def check_status(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passport_number = request.POST.get('passport_number')
        
        try:
            application = Application.objects.get(email=email, passport_number=passport_number)
            return render(request, 'xorijiy/status_result.html', {'application': application})
        except Application.DoesNotExist:
            messages.error(request, "Berilgan ma'lumotlar bo'yicha ariza topilmadi.")
    
    return render(request, 'check_status.html')