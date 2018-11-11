from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
    
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, 
                               widget=forms.Textarea)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',  widget=forms.PasswordInput())

    #password validation
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')


class MedicineForm(forms.Form):
    med_name = forms.CharField(max_length=30, label='Name', required=False)
    med_symptom = forms.CharField(max_length=50, label='Purpose', required=False)

    def clean(self):
        med_name = self.cleaned_data.get("med_name")
        med_symptom = self.cleaned_data.get("med_symptom")
        print('med_name -', med_name)
        print('med_symptom -', med_symptom)
        if (med_name != "" and med_symptom != "") or (med_symptom == "" and med_name == ""):
            print("Invalid form")
            raise forms.ValidationError('Select any one')
        else:
            pass


        #return super(MedicineForm, self).clean(*args, **kwargs)
