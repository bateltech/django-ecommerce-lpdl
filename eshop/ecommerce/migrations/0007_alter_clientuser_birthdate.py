# Generated by Django 4.2.6 on 2023-11-18 20:39

from django.db import migrations
import ecommerce.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_cart_rename_fk_user_commande_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientuser',
            name='birthdate',
            field=ecommerce.models.CustomDateFormatField(blank=True, null=True),
        ),
    ]
