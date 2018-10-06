from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    """Form to be used to login users"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    """Form used to register user"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u"Email address must be unique")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        """
        The following validation is also handled by bootstrap forms
        so this validation error will not raise as validation error
        from bootstrap form will be raised beforehand, hence
        this validation will not be covered by tests when bootstrap
        form is used.
        """
        if not password1 or not password2:
            raise forms.ValidationError(u"Please confirm your password")

        if password1 != password2:
            raise forms.ValidationError(u"Password must match")

        return password2
