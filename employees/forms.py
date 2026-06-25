from django import forms
from .models import IshAriza


class IshArizaForm(forms.ModelForm):
    class Meta:
        model = IshAriza
        fields = [
            'full_name', 'phone', 'email',
            'nationality', 'nationality_other',
            'address', 'birth_date', 'education_level',
            'education_diploma', 'academic_title', 'academic_degree',
            'foreign_language', 'institution',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Masalan: Usmonov Erkin Baxtiyorovich"
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "+998 90 123 45 67"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': "example@gmail.com"
            }),
            'nationality': forms.Select(attrs={'class': 'form-select', 'id': 'id_nationality'}),
            'nationality_other': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Millatingizni kiriting"
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Viloyat, tuman, ko'cha, uy"
            }),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'education_diploma': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
            'academic_title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Masalan: Dotsent"
            }),
            'academic_degree': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Masalan: Falsafa doktori (PhD)"
            }),
            'foreign_language': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Masalan: Ingliz tili — B2 (IELTS 6.0)"
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "Olgan ta'lim muassasangiz nomi"
            }),
        }
        labels = {
            'full_name': "Familiya, ism, sharifingiz",
            'phone': "Telefon raqamingiz",
            'email': "Email manzilingiz",
            'nationality': "Millatingiz",
            'nationality_other': "Boshqa (millatingizni kiriting)",
            'address': "Yashash manzilingiz",
            'birth_date': "Tug'ilgan sanangiz",
            'education_level': "Ma'lumotingiz",
            'education_diploma': "Ta'lim diplomi fayli",
            'academic_title': "Ilmiy unvoningiz",
            'academic_degree': "Ilmiy darajangiz",
            'foreign_language': "Xorijiy tillarni bilish darajasi",
            'institution': "Ta'lim muassasasi",
        }
