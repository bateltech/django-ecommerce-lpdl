from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ClientUser, Voyance
from django.contrib.admin.widgets import AdminDateWidget

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define a dictionary to hold custom attributes and classes for each field
        custom_attributes = {
            'username': {'class': 'custom-email-class', 'placeholder': ' Entrez votre adresse email'},
            'password': {'type': 'password', 'class': 'custom-password-class', 'placeholder': ' Entrez votre mot de passe'},
        }
        
        # Update each field's attributes and classes
        for field_name, attributes in custom_attributes.items():
            self.fields[field_name].widget.attrs.update(attributes)


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
          model = ClientUser
          fields = ["first_name", "last_name", "email", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define a dictionary to hold custom attributes and classes for each field
        custom_attributes = {
            'first_name': {'class': 'custom-first-name-class', 'placeholder': ' Votre prénom'},
            'last_name': {'class': 'custom-last-name-class', 'placeholder': ' Votre nom'},
            'email': {'class': 'custom-email-class', 'placeholder': ' Entrez votre adresse email'},
            'password1': {'type': 'password', 'class': 'custom-password-class', 'placeholder': ' Entrez votre mot de passe'},
            'password2': {'type': 'password', 'class': 'custom-password-class', 'placeholder': ' Confirmez votre mot de passe'},
        }
    

        # Update each field's attributes and classes
        for field_name, attributes in custom_attributes.items():
            self.fields[field_name].widget.attrs.update(attributes)


from django.forms import DateInput
import phonenumbers
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError

class DatePickerInput(DateInput):
    input_type = 'date'
    format_key = 'DATE_INPUT_FORMATS'
    format = ['%d/%m/%Y']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = ClientUser
        fields = ['last_name', 'first_name', 'birthdate', 'email', 'phone_number']

    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'custom-name-class','placeholder': 'Votre nom'}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'custom-name-class','placeholder': 'Votre prénom'}))
    birthdate = forms.DateField(widget=DatePickerInput(attrs={'class': 'custom-date-class','placeholder': 'jj/mm/AAAA'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-mail-class','placeholder': 'Votre adresse email'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'custom-phone-class', 'id': 'phone_number', 'placeholder': '06 60 00 00 60'}))


from django.contrib.auth.forms import PasswordChangeForm

class PasswordResetForm(PasswordChangeForm):

    class Meta:
        model = ClientUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajouter des classes aux champs
        self.fields['old_password'].widget.attrs['class'] = 'custom-class-old-password'
        self.fields['new_password1'].widget.attrs['class'] = 'custom-class-new-password1'
        self.fields['new_password2'].widget.attrs['class'] = 'custom-class-new-password2'

        # Ajouter des placeholders
        self.fields['old_password'].widget.attrs['placeholder'] = ' votre mot de passe actuel'
        self.fields['new_password1'].widget.attrs['placeholder'] = ' votre nouveau mot de passe'
        self.fields['new_password2'].widget.attrs['placeholder'] = ' confirmer votre nouveau mot de passe'


class VoyanceForm(forms.ModelForm):
    class Meta:
        model = Voyance
        fields = ['nom', 'prenom', 'email', 'image', 'contenu_demande']

    nom = forms.CharField(label='Nom', max_length=100, required=True, widget=forms.TextInput(attrs={'id': 'nom'}))
    prenom = forms.CharField(label='Prénom', max_length=100, required=True, widget=forms.TextInput(attrs={'id': 'prenom'}))
    email = forms.EmailField(label='Email', max_length=100, required=True, widget=forms.EmailInput(attrs={'id': 'email','readonly': 'readonly'}))
    image = forms.ImageField(label='Photo', required=True, widget=forms.FileInput(attrs={'id': 'image', 'class': 'form__image', 'accept': 'image/*', 'onchange': 'previewImage(event)'}))
    contenu_demande = forms.CharField(label='Contenu de la demande', widget=forms.Textarea(attrs={'id': 'contenu', 'rows': '8'}), required=True)



from django_ckeditor_5.fields import CKEditor5Field

class NewsletterForm(forms.Form):
    subject = forms.CharField()
    message = CKEditor5Field()