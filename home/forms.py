from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Your full name", 'name': 'name', 'id': 'name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': "form-control", 'name': 'email', 'id': 'email'}))
    phone_num = forms.CharField(max_length=15, label="Contact Number", widget=forms.TextInput(
        attrs={'class': "form-control", 'name': 'phone', 'id': 'phone'}))
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(
        attrs={'type': 'date', 'class': "form-control", 'name': 'dob', 'id': 'dob'}))
    street = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': "form-control", 'name': 'street', 'id': 'street'}))
    house_no = forms.CharField(max_length=20, label="House Number", widget=forms.TextInput(
        attrs={'class': "form-control", 'name': 'house_no', 'id': 'house_no'}))
    area = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': "form-control", 'name': 'area', 'id': 'area'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Username can contain alphanumeric and underscore only",
             'name': 'username', 'id': 'username'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Password must contain at least 9 characters", 'name': 'password1',
             'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'name': 'password2', 'id': 'password2'})

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'email', 'phone_num', 'dob', 'street', 'house_no',
                  'area']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'name': 'username', 'id': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control", 'name': 'password', 'id': 'password'}))
