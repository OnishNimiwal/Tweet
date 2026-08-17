from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['text','photo','video']





class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('email','username','password1','password2')#here we have to use the tuple as using the built in forms
        
        


class SearchTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Search Tweet...'
            })
        }