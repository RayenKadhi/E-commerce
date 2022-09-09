from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreation(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreation,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control'})



    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','password1', 'password2']

