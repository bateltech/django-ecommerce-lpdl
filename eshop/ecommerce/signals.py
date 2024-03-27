from .views import sendEmail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Newsletter

# Recepteur
@receiver(post_save, sender=Newsletter)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        # Appeler la vue sendEmail avec les données de l'objet Newsletter
        sendEmail(instance.subject, instance.message)