from .views import sendEmail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

# Recepteur
@receiver(post_save, sender=Newsletter)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        # Appeler la vue sendEmail avec les données de l'objet Newsletter
        sendEmail(instance.subject, instance.message)

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.db import models
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

@receiver(post_save, sender=Commande)
def send_payment_confirmation_email(sender, instance, **kwargs):
    print("trying to send an email to the customer outside")
    print("instance.etat : ", instance.etat)

    if instance.etat == 'payee':
        print("trying to send an email to the customer")
        # get the list of detail commandes
        detail_commandes = instance.detailcommande_set.all()

        # build the email context
        context = {
            'commande': instance,
            'detail_commandes': detail_commandes,
            'LOGO_BASE64': settings.LOGO_BASE64,
        }

        # render the email template
        subject = 'Commande {} - Confirmation de paiement'.format(instance.id)
        message = render_to_string('payment_confirmation.html', context)

        # send the email
        send_mail(
            subject=subject,
            message=message,
            from_email= f'Pierre de Lune <{settings.EMAIL_HOST_USER}>',
            recipient_list=[instance.user.email],
            fail_silently=False,
            html_message=message,
        )

@receiver(models.signals.post_save, sender=Commande)
def send_admin_new_commande_email(sender, instance, **kwargs):
    print("trying to send an email to the admin outside")

    if  instance.etat == 'payee':
        print("trying to send an email for the admin")
        # get the list of detail commandes
        detail_commandes = instance.detailcommande_set.all()

        # build the email context
        context = {
            'commande': instance,
            'detail_commandes': detail_commandes,
            'LOGO_BASE64': settings.LOGO_BASE64,
        }

        # render the email template
        subject = 'Nouvelle commande reçue - Commande {}'.format(instance.id)
        message = render_to_string('admin_new_commande.html', context)
        print("email content : ", message)

        # send the email
        send_mail(
            subject=subject,
            message=message,
            from_email= f'Pierre de Lune <{settings.EMAIL_HOST_USER}>',
            recipient_list=[settings.EMAIL_RECIPIENT],
            fail_silently=False,
            html_message=message,
        )

##############################################################################################################

@receiver(post_save, sender=DemandeVoyance)
def send_payment_confirmation_voyance_email(sender, instance, **kwargs):
    print("trying to send an email to the customer outside")
    print("instance.etat : ", instance.etat)

    if instance.etat == 'payee':
        print("trying to send an email to the customer")

        # get the voyance description
        voyance = Voyance.objects.filter(type=instance.type).first()
        
        # build the email context
        context = {
            'commande': instance,
            'voyance': voyance,
            'LOGO_BASE64': settings.LOGO_BASE64,
            'adresse_voyance': settings.ADRESSE_VOYANCE
        }

        # render the email template
        subject = ' Voyance {} - Confirmation de paiement'.format(instance.id)
        message = render_to_string('payment_confirmation_voyance.html', context)

        # send the email
        send_mail(
            subject=subject,
            message=message,
            from_email= f'Pierre de Lune <{settings.EMAIL_HOST_USER}>',
            recipient_list=[instance.user.email],
            fail_silently=False,
            html_message=message,
        )

@receiver(models.signals.post_save, sender=DemandeVoyance)
def send_admin_new_voyance_email(sender, instance, **kwargs):
    print("trying to send an email to the admin outside")

    if  instance.etat == 'payee':
        print("trying to send an email for the admin")

        # get the voyance description
        voyance = Voyance.objects.filter(type=instance.type).first()

        # build the email context
        context = {
            'commande': instance,
            'voyance': voyance,
            'LOGO_BASE64': settings.LOGO_BASE64,
        }

        # render the email template
        subject = 'Nouvelle voyance payée - Voyance {}'.format(instance.id)
        message = render_to_string('admin_new_voyance.html', context)
        print("email content : ", message)

        # send the email
        send_mail(
            subject=subject,
            message=message,
            from_email= f'Pierre de Lune <{settings.EMAIL_HOST_USER}>',
            recipient_list=[settings.EMAIL_RECIPIENT],
            fail_silently=False,
            html_message=message,
        )

##############################################################################################################
