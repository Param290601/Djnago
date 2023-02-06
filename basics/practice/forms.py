from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'First name', 'aria-describedby':'helpId'}),

            'email' : forms.EmailInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'Example@gmail.com', 'aria-describedby':'helpId'}),

            'password1' : forms.PasswordInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'Example@gmail.com', 'aria-describedby':'helpId'}),

            'password2' : forms.PasswordInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'******', 'aria-describedby':'helpId'})
        }
 
        