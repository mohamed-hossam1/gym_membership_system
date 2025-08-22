from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'age', 'phone', 'subscription_start_date', 'subscription_end_date', 'image']
        
        widgets = {
            'subscription_start_date': forms.DateInput(attrs={'type': 'date'}),
            'subscription_end_date': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter member\'s full name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Enter age'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone number'}),
        }

