from django.contrib.auth.forms import UsernameField
from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class LAWAuthenticationForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput()
    )
    client_id = forms.CharField(
        label="Client Id", strip=False, widget=forms.PasswordInput()
    )
    client_secret = forms.CharField(
        label="Client Secret", strip=False, widget=forms.PasswordInput()
    )
