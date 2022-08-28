from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm,forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class CreateUser(UserCreationForm):

    class Meta:
        model = User
        fields = [ 'email','username','first_name','last_name','password1','password2']


class BranchUser(UserCreationForm):

    class Meta:
        model = User
        fields = [ 'username','password1','password2']




