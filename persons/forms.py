from django.contrib.auth.models import User
from .models import Person
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirma Password')

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
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICE, label='Genero',)
    name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Teléfono',
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label='Edad', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Person
        fields = ['name', 'email', 'phone', 'age', 'gender']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = Person.objects.filter(email=email)
        if email_qs.exists():
            if self.instance.pk != email_qs[0].pk:
                raise forms.ValidationError("Este email ya ha sido registrado")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if (age > 110) or (0 > age):
            raise forms.ValidationError("Edad inávlida")
        return age
