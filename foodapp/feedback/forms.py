from allauth.account.forms import SignupForm
from django import forms

class UserSignUpForm(SignupForm):
    username = forms.CharField(max_length=50, label='Username')
    first_name = forms.CharField(max_length=50, label='First name')
    last_name = forms.CharField(max_length=50, label='Last name')
    email = forms.CharField(max_length=50, label='Email address')

    def save(self, request):
        user = super(UserSignUpForm, self).save(request)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_user = True
        user.save()
        return user

class AdminSignUpForm(SignupForm):
    username = forms.CharField(max_length=50, label='Username')
    first_name = forms.CharField(max_length=50, label='First name')
    last_name = forms.CharField(max_length=50, label='Last name')
    email = forms.CharField(max_length=50, label='Email address')

    def save(self, request):
        user = super(AdminSignUpForm, self).save(request)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_admin = True
        user.save()
        return user