from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_cart_rename_fk_user_commande_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('libelle', models.CharField(
                    default='',
                    max_length=128,
                    verbose_name='Nom'
                )),
                ('description', models.TextField()),
                ('image', models.ImageField(
                    default='',
                    upload_to='collections/'
                )),
                ('disponible', models.BooleanField(
                    default=False,
                    verbose_name='Disponible'
                )),
            ],
        ),
        migrations.CreateModel(
            name='DetailCollection',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('article', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='ecommerce.article'
                )),
                ('collection', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='ecommerce.collection'
                )),
            ],
        ),
        migrations.AddConstraint(
            model_name='detailcollection',
            constraint=models.UniqueConstraint(
                fields=('collection', 'article'),
                name='unique_collection_article'
            ),
        ),
        migrations.AddField(
            model_name='collection',
            name='articles',
            field=models.ManyToManyField(
                through='ecommerce.DetailCollection',
                to='ecommerce.article'
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='Date de création'
            ),
            preserve_default=False,
        ),
    ]