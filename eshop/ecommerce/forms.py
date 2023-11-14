from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ClientUser



class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
          model = ClientUser
          fields = ["first_name", "last_name", "email", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define a dictionary to hold custom attributes and classes for each field
        custom_attributes = {
            'first_name': {'class': 'custom-first-name-class', 'placeholder': ' Entrez votre prénom'},
            'last_name': {'class': 'custom-last-name-class', 'placeholder': ' Entrez votre nom'},
            'email': {'class': 'custom-email-class', 'placeholder': ' Entrez votre adresse email'},
            'password1': {'type': 'password', 'class': 'custom-password-class', 'placeholder': ' Entrez votre mot de passe'},
            'password2': {'type': 'password', 'class': 'custom-password-class', 'placeholder': ' Confirmez votre mot de passe'},
        }
        
        # Update each field's attributes and classes
        for field_name, attributes in custom_attributes.items():
            self.fields[field_name].widget.attrs.update(attributes)


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
