from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class UserRegisterForm(UserCreationForm):
    imie = forms.CharField(max_length=200)
    nazwisko = forms.CharField(max_length=200)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','imie','nazwisko', 'password1', 'password2']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']

class KomentarzForm(ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
        labels = {
            'tresc': '',
        }
        widgets = {
          'tresc': forms.Textarea(attrs={'rows':1, 'cols':45, 'placeholder': 'Skomentuj post'},),
        }


class NowyPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['tytul','tekst','obrazek']


