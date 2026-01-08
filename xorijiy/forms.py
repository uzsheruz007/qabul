from django import forms
from .models import ForeignStudentRequest

class ForeignStudentRequestForm(forms.ModelForm):
    class Meta:
        model = ForeignStudentRequest
        fields = [
            'full_name',
            'country',
            'email',
            'phone',
            'faculty',
            'message'
        ]
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Savolingiz yoki murojaatingizni yozing'
            })
        }
