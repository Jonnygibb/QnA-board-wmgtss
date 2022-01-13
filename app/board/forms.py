from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    """
    Form representing sign in webpage
    """
    # Field for password input - typed characters will be hidden
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        # User model from models.py
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class LogInForm(forms.ModelForm):
    """
    Form representing login webpage
    """
    # Field for password input - typed characters will be hidden
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        # User model from models.py
        model = User
        fields = ['email', 'password']
