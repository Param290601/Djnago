from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'********', 'aria-describedby':'helpId', 'type':'password'}))
    password2 = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'******', 'aria-describedby':'helpId','type':'password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'First name', 'aria-describedby':'helpId'}),

            'email' : forms.EmailInput(attrs={'class':'form-control rounded-pill',
                           'placeholder':'Example@gmail.com', 'aria-describedby':'helpId'}),

            # 'password1' : forms.TextInput(attrs={'class':'form-control rounded-pill',
            #                'placeholder':'********', 'aria-describedby':'helpId', 'type':'password'}),

            # 'password2' : forms.PasswordInput(attrs={'class':'form-control rounded-pill',
            #                'placeholder':'******', 'aria-describedby':'helpId'})
        }

    def clean_username(self):
        first_name = self.cleaned_data['username']        
        if first_name == "":            
            raise forms.ValidationError("First name is required!")        
        if not first_name.isalpha():            
            raise forms.ValidationError("Invalid First name!")        
        return first_name  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email is already exsist")
        return email

    # def clean(self):
    #     cleaned_data =  super().clean()
        # name = self.cleaned_data['username']
        # if name.isnumeric():
        #     raise forms.ValidationError("numbers are not valid in username")
        # email = self.cleaned_data['email']
        # if User.objects.get(email = email):
        #     raise forms.ValidationError("Email is already exsist")
        # password = self.cleaned_data['password1']
        # if len(password) < 5:
        #     raise forms.ValidationError('password should be greater than 5')
            