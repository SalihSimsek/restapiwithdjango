from django.contrib.auth import authenticate

from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django import forms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text = 'Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ('email','username','first_name','last_name','password1','password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,label = 'Kullanıcı Adı')
    password = forms.CharField(max_length=100,label = 'Parola',widget = forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('Kullanıcı adı veya şifre hatalı')
            return super(LoginForm,self).clean()

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email','username','first_name','last_name')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email {} is already use.'.format(account.email))

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username'].lower()
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username {} is already in use'.format(account.username))