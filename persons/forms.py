from django.contrib.auth.models import User
from .models import Person
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirma Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Los password deben ser iguales")


class PersonForm(forms.ModelForm):
    CHOICE = (('Femenino', 'Femenino'), ('Masculino', 'Masculino'))
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICE, label='Genero')
    name = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Teléfono')
    age = forms.IntegerField(label='Edad')

    class Meta:
        model = Person
        fields = ['name', 'email', 'phone', 'age', 'gender']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = Person.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Este email ha sido registrado")
        return email