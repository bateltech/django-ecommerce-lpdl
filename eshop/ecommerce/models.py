from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


# class CustomDateFormatField(models.DateField):
#     def to_python(self, value):
#         if value:
#             return datetime.strptime(value, '%d/%m/%Y').date()
#         return None

# Table Client
class ClientUser(AbstractUser):
    # Ajoutez des champs d'utilisateur personnalisés si nécessaire
     # New fields
    phone_number = PhoneNumberField(null=True, blank=True)
    #birthdate = CustomDateFormatField(null=True, blank=True)
    
    birthdate = models.DateField(null=True, blank=True)
    
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
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle


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

    taille = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)

    def __str__(self):
        if self.type_prix == 'size_based':
            return f"{self.taille}cm - {self.prix} €"
        else:
            return f"{self.get_type_prix_display()} - {self.prix} €"
    

# Table Article
class Article(models.Model):
    libelle = models.CharField(max_length=128, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    stock = models.IntegerField(default=0, null=False)
    prix_article = models.ManyToManyField(PrixArticle, related_name='articles')  # Many-to-Many relationship with PrixArticle
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagBesoin, related_name='articles', blank=True)  # Many-to-Many relationship with Tag
    pierres = models.ManyToManyField(Pierre, related_name='articles', blank=True)  # Many-to-Many relationship with Pierre
    #  when I want to access all the articles related to an instance of a tag or pierre,
    #  I should use this : my_tag.articles.all() that's what related_name is for

    def __str__(self):
        return self.libelle


# not used in code 
# Table Taille Article
class TailleArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    taille = models.IntegerField()

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
        
        self.item_price = self.article_price.prix
        self.total_item_price = self.article_price.prix * self.quantity
        
        super().save(*args, **kwargs)

# Table Commande
class Commande(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='DetailCommande')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('payee', 'Payée')], default='en attente')
    telephone = models.CharField(max_length=20, null=False)
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100, null=False)
    numero_rue = models.CharField(max_length=100, null=False)
    adresse = models.CharField(max_length=255, null=False)
    ville = models.CharField(max_length=100, null=False)
    code_postal = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=255, null=False)
    session_id = models.CharField(max_length=250,blank=True, null=True)
    payment_intent = models.CharField(max_length=250,blank=True, null=True)


    def __str__(self):
        if self.etat == "en attente" :
            return f"En Attente || Commande pour {self.user.username}"
        
        if self.etat == "payee":
            return f"Payée || Commande pour {self.user.username}" 

# Table Détail Commande
class DetailCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# Table Feedback
class Feedback(models.Model):
    contenu = models.TextField(null=False)
    date_envoi = models.DateField(null=False)
    utilisateur = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    etat = models.IntegerField(null=False,default=0)

    def __str__(self):
        return f"Feedback #{self.id} de {self.utilisateur.last_name} {self.utilisateur.first_name}"


from datetime import timedelta
# Table Voyance
class Voyance(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='images/')
    contenu_demande = models.TextField()
    tarif = models.FloatField(default=30.00)
    etat = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('payee', 'Payée')], default='en attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_created_at_plus_six_days(self):
        return self.created_at + timedelta(days=6)


from django_ckeditor_5.fields import CKEditor5Field

# Table Newsletter
class Newsletter(models.Model):
    subject = models.TextField(max_length=128)
    message = CKEditor5Field(config_name='newsletter')
    image_urls = models.TextField(blank=True, editable=False)

    def __str__(self) -> str:
        return f"{self.subject}"
    

# Table DemandeVoyance
class DemandeVoyance(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('payee', 'Payée')], default='en attente')
    telephone = models.CharField(max_length=20, null=False)
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, null=False)
    session_id = models.CharField(max_length=250,blank=True, null=True)
    payment_intent = models.CharField(max_length=250,blank=True, null=True)


    def __str__(self):
        return f"Voyance pour {self.prenom} {self.nom}"
