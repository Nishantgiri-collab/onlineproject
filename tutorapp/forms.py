from django import forms
from .models import RegistrationUser, ClassSlot

class RegistrationUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = RegistrationUser
        fields = [
            'fullname',
            'phone_number',
            'age',
            'previous_qualification',
            'previous_qualification_percentage',
            'email',
            'password',
            'confirm_password',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)





class ClassBookingForm(forms.ModelForm):
    class Meta:
        model = ClassSlot
        fields = ['slot']
        widgets = {
            'slot': forms.Select(attrs={'class': 'form-select'}),
        }