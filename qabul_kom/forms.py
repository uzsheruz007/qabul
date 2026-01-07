from django import forms
from .models import Document, DocumentCategory

class DocumentSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Qidirish',
        widget=forms.TextInput(attrs={
            'placeholder': 'Hujjat nomi bo\'yicha qidirish...',
            'class': 'form-control'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False,
        label='Kategoriya',
        widget=forms.Select(attrs={'class': 'form-control'})
    )