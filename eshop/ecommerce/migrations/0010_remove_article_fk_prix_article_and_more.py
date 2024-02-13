# Generated by Django 4.2.6 on 2024-02-01 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_rename_max_size_prixarticle_taille_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='fk_prix_article',
        ),
        migrations.AddField(
            model_name='article',
            name='fk_prix_article',
            field=models.ManyToManyField(related_name='articles', to='ecommerce.prixarticle'),
        ),
    ]