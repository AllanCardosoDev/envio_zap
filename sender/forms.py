from django import forms
from .models import Contact, Group

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+5599999-9999'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members']
