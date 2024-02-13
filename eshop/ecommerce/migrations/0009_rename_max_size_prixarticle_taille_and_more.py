# Generated by Django 4.2.6 on 2024-01-14 18:24

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_alter_clientuser_birthdate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prixarticle',
            old_name='max_size',
            new_name='taille',
        ),
        migrations.RemoveField(
            model_name='article',
            name='fk_pierre',
        ),
        migrations.RemoveField(
            model_name='article',
            name='fk_tag',
        ),
        migrations.RemoveField(
            model_name='prixarticle',
            name='min_size',
        ),
        migrations.AddField(
            model_name='article',
            name='pierres',
            field=models.ManyToManyField(related_name='articles', to='ecommerce.pierre'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='articles', to='ecommerce.tagbesoin'),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]