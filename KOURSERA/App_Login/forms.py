from django import forms
from .models import User,Profile
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    ''' FORM FOR FILL THE PROFILE INFORMATION '''
    ''' USER FIELD WILL BE AUTO FILLED WHILE REGISTRATION '''

    class Meta:
        model = Profile
        exclude = ('user',)


class SignUpForm(UserCreationForm):
    ''' CREATE USER WITH JUST EMAIL AND PASSWORD '''

    class Meta:
        model = User
        fields = ('email','password1','password2') 