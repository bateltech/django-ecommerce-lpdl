from django.contrib import admin
from .models import Article, Commande, Promo, VIPromo, Collection, DetailCommande, Pierre, PrixArticle, TagBesoin, Categorie, SousCategorie, Commentaire, Feedback, ClientUser, Wishlist
from .models import Newsletter

#####################################################################################
# FULL PERMISSION TABLES

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', 'pierres')  # Display tags and pierres as checkboxes
    list_display = ('libelle', 'stock', 'categorie')

    def categorie(self, obj):
        return obj.categorie.libelle
    
@admin.register(PrixArticle)
class PrixArticleAdmin(admin.ModelAdmin):
    list_display = ('prix_article', 'type_prix')

    def prix_article(self, obj):
        if obj.type_prix == 'size_based':
            return f"{obj.taille} cm - {obj.prix} €"
        else:
            return f"{obj.prix} €"

    prix_article.short_description = 'Prix Article'


class ArticleInline(admin.TabularInline):
    model = Collection.articles.through  # Use the through model of the ManyToMany relationship
    extra = 0
    verbose_name = "Article"
    verbose_name_plural = "Articles"

    def get_queryset(self, request):
        # Fetch the collection from the parent object being viewed
        collection_id = request.resolver_match.kwargs.get('object_id')
        if collection_id:
            return super().get_queryset(request).filter(collection_id=collection_id)
        return super().get_queryset(request)
    
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
    list_display = ('libelle','disponible')
    readonly_fields = ('articles',)
    
admin.site.register(Pierre)
admin.site.register(TagBesoin)
admin.site.register(Categorie)
admin.site.register(SousCategorie)
admin.site.register(Promo)
admin.site.register(VIPromo)

#####################################################################################
# EDIT-ONE-FIELD-ONLY TABLES

# admin.site.register(Commentaire) # pour la version 2
@admin.register(Feedback)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'etat')
    readonly_fields = ('contenu', 'date_envoi', 'utilisateur')
    
    def feedback(self, obj):
        return "Feedback N°{}" .format(obj.id)
    feedback.short_description = 'Feedback'

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    

#####################################################################################
# READONLY TABLES

from django.contrib.auth.admin import UserAdmin
from django import forms

@admin.register(ClientUser)
class ClientUserAdmin(UserAdmin):

    readonly_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'birthdate')
    
    def get_fields(self, request, obj=None):
        return ['username', 'first_name', 'last_name', 'email', 'phone_number', 'birthdate']
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

class DetailCommandeInline(admin.TabularInline):
    model = DetailCommande
    extra = 1
    readonly_fields = ('commande', 'article','quantity', 'item_price', 'size')

    verbose_name_plural = "Détails de la commande"  # Optionally change the verbose name of the inline


    def quantity(self, obj):
        return obj.quantity

    def item_price(self, obj):
        return "{} €".format(obj.item_price)

    def size(self, obj):
        return "{} cm".format(obj.size)
    
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    inlines = [DetailCommandeInline]
    readonly_fields = ('user', 'total_price', 'created_at', 'etat', 'telephone', 'nom', 'prenom', 'numero_rue', 'adresse', 'ville', 'code_postal', 'email','promoVIP', 'session_id', 'payment_intent')
    list_display = ('commande_numero', 'montant_total', 'etat', 'date_created')
    list_filter =('etat', 'created_at')

    def get_fields(self, request, obj=None):
        if obj:
            return ['etat', 'user', 'nom', 'prenom', 'telephone', 'email', 'numero_rue', 'adresse', 'ville', 'code_postal', 'promoVIP']
        return []

    def commande_numero(self, obj):
        return "Commande N°{}" .format(obj.id)
    commande_numero.short_description = 'Commande'

    def montant_total(self, obj):
        return "{} €" .format(obj.total_price)
    montant_total.short_description = 'Montant total'

    def date_created(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")
    date_created.short_description = 'Date'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

# Optionally, you can also register DetailCommande to make it available separately
@admin.register(DetailCommande)
class DetailCommandeAdmin(admin.ModelAdmin):
    list_display = ['commande', 'article', 'quantite', 'prix', 'taille']
    list_filter = ['commande', 'article']

    def quantite(self, obj):
        return "{}" .format(obj.quantity)
    quantite.short_description = "Quantité"

    def taille(self, obj):
        if obj.size is None:
            return " - "
        return "{} cm" .format(obj.size)
    taille.short_description = "Taille"

    def prix(self, obj):
        return "{} €" .format(obj.item_price)
    prix.short_description = "Prix d'article"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False




# admin.site.register(Newsletter)