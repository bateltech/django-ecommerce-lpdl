from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Table Client
class ClientUser(AbstractUser):
    # Ajoutez des champs d'utilisateur personnalisés si nécessaire
     # New fields
    phone_number = PhoneNumberField(null=True, blank=True, verbose_name="N° de téléphone")
    VIP = models.BooleanField(default=False, verbose_name="VIP")
    birthdate = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    
    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(Group, related_name='client_users')
    user_permissions = models.ManyToManyField(
        Permission, related_name='client_users_permissions')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def save(self, *args, **kwargs):
    # Check if the username is empty
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


# Table Pierre
class Pierre(models.Model):
    libelle = models.CharField(max_length=255, null=False, verbose_name="Libellé")
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='pierres/', null=False)
    couverture = models.ImageField(upload_to='covers/', null=False)
    def __str__(self):
        return self.libelle

    def save(self, *args, **kwargs):
        if self.image and not is_webp_image(self.image):
            self.image = convert_to_webp(self.image)
        if self.couverture and not is_webp_image(self.couverture):
            self.couverture = convert_to_webp(self.couverture)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        if self.couverture:
            self.couverture.delete(save=False)
        super().delete(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="100" height="100" />' % (self.image.url))
        else:
            return 'Aucune photo'

    image_tag.short_description = 'Aperçu de la photo'
    image_tag.allow_tags = True

    def cover_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="100" />' % (self.couverture.url))
        else:
            return 'Aucune couverture'

    cover_tag.short_description = 'Aperçu de la couverture'
    cover_tag.allow_tags = True


@receiver(post_delete, sender=Pierre)
def delete_pierre_images(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.couverture:
        instance.couverture.delete(save=False)

# Table Catégorie
class Categorie(models.Model):
    libelle = models.CharField(max_length=255, null=False, verbose_name="Nom")

    def __str__(self):
        return self.libelle
    
    class Meta:
        verbose_name = "Catégorie"


# Table Sous Catégorie
class SousCategorie(models.Model):
    libelle = models.CharField(max_length=255, null=False, verbose_name="Libellé")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name="Catégorie")

    def __str__(self):
        return self.libelle
    
    class Meta:
        verbose_name = "Sous-catégorie"


# Table Commentaire
class Commentaire(models.Model):
    contenu = models.TextField(null=False)
    utilisateur = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    etat = models.IntegerField(null=False,default=0)
    date_envoi = models.DateField(null=False)


    def __str__(self):
        return f"Commentaire #{self.id} par {self.utilisateur.username}"


# Table Tag par besoin
class TagBesoin(models.Model):
    libelle = models.CharField(max_length=255, null=False, verbose_name="Libellé")

    def __str__(self):
        return self.libelle


# Table Prix Article
class PrixArticle(models.Model):
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixe'),
        ('size_based', 'Par taille'),
    ]

    type_prix = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='fixed')
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)

    taille = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)

    def __str__(self):
        if self.type_prix == 'size_based':
            return f"{self.taille}cm - {self.prix} €"
        else:
            return f"{self.get_type_prix_display()} - {self.prix} €"
    

from django.utils import timezone as timez
# Table Article
class Article(models.Model):
    libelle = models.CharField(max_length=128, null=False, verbose_name="Nom")
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    image = models.ImageField(upload_to="articles/", null=False)
    stock = models.IntegerField(default=0, null=False)
    prix_article = models.ManyToManyField(PrixArticle, related_name='articles')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name='Catégorie')
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, verbose_name='Sous-catégorie')
    tags = models.ManyToManyField(TagBesoin, related_name='articles', blank=True)
    pierres = models.ManyToManyField(Pierre, related_name='articles', blank=True)
    #  when I want to access all the articles related to an instance of a tag or pierre,
    #  I should use this : my_tag.articles.all() that's what related_name is for

    def __str__(self):
        return self.libelle

    def is_new(self):
        return self.created_at >= timez.now() - timedelta(days=30)
    
    def save(self, *args, **kwargs):
        if self.image and not is_webp_image(self.image):
            self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="100" height="150" />' % (self.image.url))
        else:
            return 'Aucune photo'

    image_tag.short_description = 'Aperçu de la photo'
    image_tag.allow_tags = True

@receiver(post_delete, sender=Article)
def delete_article_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


# Table Promo
from django.db import models

class Promo(models.Model):
    libelle = models.CharField(max_length=128, null=False, default="", verbose_name="Nom")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    discount_percentage = models.FloatField(verbose_name="Pourcentage de réduction")
    articles = models.ManyToManyField('Article', related_name='promos')

    def __str__(self):
        return f"Promo : {self.discount_percentage}% de réduction du {self.start_date} au {self.end_date}"

# Table VIPromo
class VIPromo(models.Model):
    discount_percentage = models.FloatField(default=10.0, verbose_name="Pourcentage de réduction")
    client = models.ForeignKey(ClientUser, on_delete=models.CASCADE, related_name='vip_promos')
    start_date = models.DateField(auto_now_add=True, verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")

    class Meta:
        verbose_name = "VIPromo"  # Singular name for the model
        verbose_name_plural = "VIPromos" # Plural name for the model

    def save(self, *args, **kwargs):
        # Set end_date to one year from start_date
        self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"VIPromo : {self.discount_percentage}% de réduction du {self.start_date} au {self.end_date} pour {self.client.email}"


# Table Collection
from django.utils.safestring import mark_safe
class Collection(models.Model):
    libelle = models.CharField(max_length=128, null=False, verbose_name="Nom")
    description = models.TextField(null=False)
    articles = models.ManyToManyField(Article, through='DetailCollection')
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    disponible = models.BooleanField(default=False, verbose_name="Disponible")

    def __str__(self):
        return f"Collection {self.libelle}"
    
    def save(self, *args, **kwargs):
        if self.image and not is_webp_image(self.image):
            self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="100" height="150" />' % (self.image.url))
        else:
            return 'Aucune photo'

    image_tag.short_description = 'Aperçu de la photo'
    image_tag.allow_tags = True

# Table DetailCollection
class DetailCollection(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['collection', 'article'], name='unique_collection_article')
        ]

@receiver(post_delete, sender=Collection)
def delete_collection_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


# Table Voyance
class Voyance(models.Model):
    libelle = models.CharField(max_length=128, null=False, verbose_name='Nom', default='')
    description = models.TextField(null=False)
    tarif = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=20, choices=[('par email', 'Par Email'), ('complete', 'Complète')], default='par email')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.libelle}"

    def get_created_at_plus_six_days(self):
        return self.created_at + timedelta(days=6)

# Table Wishlist
class Wishlist(models.Model):
    client = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return f"{self.client}'s Wishlist"
    

# Table Panier 
class Cart(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tarif_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def calculate_total_price(self):
        total_price = sum(item.item_price * item.quantity for item in self.cartitem_set.all())
        self.total_price = total_price
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# Table Item Panier
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    article_price = models.ForeignKey(PrixArticle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        
        # self.item_price = self.article_price.prix
        self.total_item_price = self.item_price * self.quantity
        
        super().save(*args, **kwargs)

# Table Commande
class Commande(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE, verbose_name='Client')
    articles = models.ManyToManyField(Article, through='DetailCommande')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant total")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    etat = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('payee', 'Payée')], default='en attente', verbose_name="État")
    telephone = models.CharField(max_length=20, null=False, verbose_name='N° de téléphone')
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100, null=False , verbose_name='Prénom')
    numero_rue = models.CharField(max_length=100, null=False, verbose_name='N° de rue')
    adresse = models.CharField(max_length=255, null=False)
    ville = models.CharField(max_length=100, null=False)
    code_postal = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=255, null=False)
    promoVIP = models.BooleanField(default=False)
    session_id = models.CharField(max_length=250,blank=True, null=True)
    payment_intent = models.CharField(max_length=250,blank=True, null=True)


    def __str__(self):
        return f"Commande N° {self.id} "


# Table Détail Commande
class DetailCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    size = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, verbose_name="Taille")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# Table Feedback
class Feedback(models.Model):
    contenu = models.TextField(null=False)
    date_envoi = models.DateField(null=False)
    utilisateur = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    etat = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('publie', 'Publié')], default='en attente', verbose_name='État')

    def __str__(self):
        return f"Feedback #{self.id} de {self.utilisateur.last_name} {self.utilisateur.first_name}"


# Table DemandeVoyance
class DemandeVoyance(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    voyance = models.CharField(max_length=128, null=False, verbose_name='Nom', default='')
    type = models.CharField(max_length=20, choices=[('par email', 'Par Email'), ('complete', 'Complète')], verbose_name='Type', default='par email')
    etat = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('payee', 'Payée')], default='en attente')
    telephone = models.CharField(max_length=20, null=False)
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, null=False)
    session_id = models.CharField(max_length=250,blank=True, null=True)
    payment_intent = models.CharField(max_length=250,blank=True, null=True)


    def __str__(self):
        return f"Voyance pour {self.prenom} {self.nom}"


from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def convert_to_webp(image_field):
    # Open the uploaded image
    uploaded_image = Image.open(image_field)

    # Convert image to WebP format
    with BytesIO() as output:
        uploaded_image.save(output, format="WEBP")
        webp_data = output.getvalue()

    # Get the original file name without extension
    original_filename = image_field.name.split('/')[-1].split('.')[0]

    # Save the WebP image data as a file object with the original filename and ".webp" extension
    webp_file = ContentFile(webp_data, name=f"{original_filename}.webp")

    return webp_file

def is_webp_image(image_field):
    return image_field.name.lower().endswith('.webp')

###############################################################################################################################################


from django_ckeditor_5.fields import CKEditor5Field

# not used for now
# Table Newsletter
class Newsletter(models.Model):
    subject = models.TextField(max_length=128)
    message = CKEditor5Field(config_name='newsletter')
    image_urls = models.TextField(blank=True, editable=False)

    def __str__(self) -> str:
        return f"{self.subject}"
    