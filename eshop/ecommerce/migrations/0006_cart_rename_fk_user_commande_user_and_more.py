# Generated by Django 4.2.6 on 2023-11-14 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_alter_pierre_couverture_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.RenameField(
            model_name='commande',
            old_name='fk_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='detailcommande',
            old_name='fk_article',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='detailcommande',
            old_name='fk_commande',
            new_name='commande',
        ),
        migrations.RenameField(
            model_name='detailcommande',
            old_name='prix',
            new_name='item_price',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='date',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='montant',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='quantite',
        ),
        migrations.AddField(
            model_name='commande',
            name='articles',
            field=models.ManyToManyField(through='ecommerce.DetailCommande', to='ecommerce.article'),
        ),
        migrations.AddField(
            model_name='commande',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commande',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='detailcommande',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.article')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.cart')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='articles',
            field=models.ManyToManyField(through='ecommerce.CartItem', to='ecommerce.article'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]