from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField

# Table Client
class ClientUser(AbstractUser):
    # Ajoutez des champs d'utilisateur personnalisés si nécessaire
     # New fields
    phone_number = PhoneNumberField(null=True, blank=True)
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



# Table Commande
class Commande(models.Model):
    fk_user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    quantite = models.PositiveIntegerField(null=False)
    etat = models.IntegerField(null=False,default=0)

    def __str__(self):
        return f"Commande #{self.id} par {self.fk_user.nom} {self.fk_user.prenom}"


# Table Détail Commande
class DetailCommande(models.Model):
    fk_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    fk_commande = models.ForeignKey('Commande', on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"DetailCommande #{self.id}"


# Table Pierre
class Pierre(models.Model):
    libelle = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='pierres/', null=False)

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


# Table Feedback
class Feedback(models.Model):
    contenu = models.TextField(null=False)
    date_envoi = models.DateField(null=False)
    fk_user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    etat = models.IntegerField(null=False,default=0)

    def __str__(self):
        return f"Feedback #{self.id} de {self.fk_user.nom} {self.fk_user.prenom}"