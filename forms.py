from django import forms
from django.contrib.auth.models import User

from .models import Feedback, User

PACKAGES = [
('', 'Please choose'),
('GOLD', 'Gold: Cost - KES 300'),
] 

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['firstname', 'lastname', 'email', 'tel','can_be_contacted','message']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'new-password','placeholder': 'Password','class':'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'autocomplete':'new-password','placeholder': 'Confirm Password','class':'form-control'}))
    tel = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '2547...','class':'form-control'}),label='Safaricom Phone No.',max_length=12)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'John','class':'form-control'}),label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Doe','class':'form-control'}),label='Last Name')
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'username','placeholder': 'johndoe','class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Valid Email','class':'form-control'}))
    package = forms.ChoiceField(choices=PACKAGES, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','tel','package','password']
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password','password_mismatch')
            

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']