from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Application, Country, StudyProgram
import datetime

class ApplicationForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="Elektron pochta tasdiqlash",
        help_text="Elektron pochtangizni qayta kiriting"
    )
    
    agree_terms = forms.BooleanField(
        label="Men shartlar va qoidalarga roziman",
        required=True,
        error_messages={'required': "Iltimos, shartlarga roziligingizni bildiring"}
    )
    
    class Meta:
        model = Application
        fields = [
            'full_name', 'date_of_birth', 'gender', 'nationality',
            'passport_number', 'passport_issue_date', 'passport_expiry_date', 'passport_photo',
            'email', 'confirm_email', 'phone', 'address', 'city', 'postal_code',
            'study_program', 'previous_education', 'previous_institution',
            'graduation_year', 'gpa', 'diploma_copy',
            'motivation_letter', 'emergency_contact_name', 'emergency_contact_phone',
            'agree_terms'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'passport_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'passport_expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'motivation_letter': forms.Textarea(attrs={'rows': 5}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'full_name': "To'liq ismingiz",
            'date_of_birth': "Tug'ilgan sanangiz",
            'gender': "Jinsingiz",
            'nationality': "Fuqaroligingiz",
            'passport_number': "Passport raqamingiz",
            'passport_issue_date': "Passport berilgan sana",
            'passport_expiry_date': "Passport amal qilish muddati",
            'passport_photo': "Passportingizning rasm nusxasi",
            'email': "Elektron pochtangiz",
            'phone': "Telefon raqamingiz",
            'address': "Yashash manzilingiz",
            'city': "Shahringiz",
            'postal_code': "Pochta indeksi",
            'study_program': "Tanlagan o'quv dasturingiz",
            'previous_education': "Oldingi ta'lim darajangiz",
            'previous_institution': "Oldingi o'quv muassasangiz",
            'graduation_year': "Bitirgan yilingiz",
            'gpa': "O'rtacha bahoingiz (GPA)",
            'diploma_copy': "Diplom nusxangiz",
            'motivation_letter': "Nima uchun bizni tanladingiz? (Motivatsion xat)",
            'emergency_contact_name': "Favqulodda vaziyat uchun aloqa shaxsi",
            'emergency_contact_phone': "Favqulodda aloqa telefon raqami",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nationality'].queryset = Country.objects.all().order_by('name')
        self.fields['study_program'].queryset = StudyProgram.objects.filter(is_active=True).order_by('name')
        
        current_year = datetime.datetime.now().year
        self.fields['graduation_year'].widget = forms.Select(
            choices=[(year, year) for year in range(current_year - 20, current_year + 1)]
        )
    
    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        
        if email and confirm_email and email != confirm_email:
            self.add_error('confirm_email', "Elektron pochta manzillari bir xil emas")
        
        date_of_birth = cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = timezone.now().date()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 16:
                self.add_error('date_of_birth', "Ariza topshirish uchun kamida 16 yoshda bo'lishingiz kerak")
        
        passport_expiry_date = cleaned_data.get('passport_expiry_date')
        if passport_expiry_date:
            today = timezone.now().date()
            if passport_expiry_date < today:
                self.add_error('passport_expiry_date', "Passportingizning amal qilish muddati tugagan")
            elif (passport_expiry_date - today).days < 180:
                self.add_error('passport_expiry_date', "Passportingizning amal qilish muddati kamida 6 oy qolishi kerak")
        
        gpa = cleaned_data.get('gpa')
        if gpa and (gpa < 0 or gpa > 4.0):
            self.add_error('gpa', "GPA 0.0 dan 4.0 gacha bo'lishi mumkin")
        
        return cleaned_data