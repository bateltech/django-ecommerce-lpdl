from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


class CustomDateFormatField(models.DateField):
    def to_python(self, value):
        if value:
            return datetime.strptime(value, '%d/%m/%Y').date()
        return None

# Table Client
class ClientUser(AbstractUser):
    # Ajoutez des champs d'utilisateur personnalisés si nécessaire
     # New fields
    phone_number = PhoneNumberField(null=True, blank=True)
    birthdate = CustomDateFormatField(null=True, blank=True)
    
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
    libelle = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='pierres/', null=False)
    couverture = models.ImageField(upload_to='covers/', null=False)
    def __str__(self):
        return self.libelle


# Table Catégorie
class Categorie(models.Model):
    libelle = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.libelle


# Table Sous Catégorie
class SousCategorie(models.Model):
    libelle = models.CharField(max_length=255, null=False)
    fk_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle


# Table Commentaire
class Commentaire(models.Model):
    contenu = models.TextField(null=False)
    fk_user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    fk_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    etat = models.IntegerField(null=False,default=0)
    date_envoi = models.DateField(null=False)


    def __str__(self):
        return f"Commentaire #{self.id} par {self.fk_user.username}"


# Table Tag par besoin
class TagBesoin(models.Model):
    libelle = models.CharField(max_length=255, null=False)

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

    min_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    max_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_prix_display()} - ${self.prix}"



# Table Article
class Article(models.Model):
    libelle = models.CharField(max_length=128, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    fk_prix_article = models.ForeignKey(PrixArticle, on_delete=models.CASCADE)
    fk_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fk_sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE)
    fk_tag = models.ForeignKey(TagBesoin, on_delete=models.CASCADE)
    fk_pierre = models.ForeignKey('Pierre', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.libelle


# Table Taille Article
class TailleArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    taille = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.article.libelle} - {self.taille}"


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

    def save(self, *args, **kwargs):
        # Calculate total price based on CartItems
        self.total_price = sum(item.quantity * item.item_price for item in self.cartitem_set.all())
        super().save(*args, **kwargs)

# Table Item Panier
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Update Cart total_price when saving CartItem
        self.cart.save()
        super().save(*args, **kwargs)

# Table Commande
class Commande(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='DetailCommande')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  
    etat = models.IntegerField(null=False,default=0)

    def save(self, *args, **kwargs):
        # Calculate total price based on DetailCommandes
        self.total_price = sum(item.quantity * item.item_price for item in self.commandeitem_set.all())
        super().save(*args, **kwargs)

# Table Détail Commande
class DetailCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Update Commande total_price when saving DetailCommande
        self.commande.save()
        super().save(*args, **kwargs)



# Table Feedback
class Feedback(models.Model):
    contenu = models.TextField(null=False)
    date_envoi = models.DateField(null=False)
    fk_user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    etat = models.IntegerField(null=False,default=0)

    def __str__(self):
        return f"Feedback #{self.id} de {self.fk_user.last_name} {self.fk_user.first_name}"