from django.contrib import admin
from .models import Article,DetailCollection , Commande, Promo, VIPromo, Collection, Voyance, DetailCommande, Pierre, PrixArticle, TagBesoin, Categorie, SousCategorie, Commentaire, Feedback, ClientUser, Wishlist
from .models import Newsletter

#####################################################################################
# FULL PERMISSION TABLES

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', 'pierres')  # Display tags and pierres as checkboxes
    list_display = ('libelle', 'stock', 'categorie', 'date_created')
    readonly_fields =('created_at', 'image_tag',)  

    def categorie(self, obj):
        return obj.categorie.libelle
    
    def date_created(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")
    
    fieldsets = (
        (None, {
            'fields': ('libelle', 'description', 'image', 'image_tag', 'stock', 'prix_article', 'categorie', 'sous_categorie', 'tags', 'pierres', 'created_at')
        }),
    )
    
@admin.register(PrixArticle)
class PrixArticleAdmin(admin.ModelAdmin):
    list_display = ('prix_article', 'type_prix')

    def prix_article(self, obj):
        if obj.type_prix == 'size_based':
            return f"{obj.taille} cm - {obj.prix} €"
        else:
            return f"{obj.prix} €"

    prix_article.short_description = 'Prix Article'

class DetailCollectionInline(admin.TabularInline):
    model = DetailCollection
    extra = 1
    verbose_name = "Article"
    verbose_name_plural = "Articles"

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CollectionForm(forms.ModelForm):
    articles = forms.ModelMultipleChoiceField(queryset=Article.objects.all(), widget=forms.SelectMultiple, required=False)

    class Meta:
        model = Collection
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        articles = cleaned_data.get('articles')
        instance = self.instance

        if articles and instance.pk:
            existing_articles = instance.articles.all()
            for article in articles:
                if article in existing_articles:
                    self.add_error('articles', _("L'article '{article}' est déjà associé à cette collection."))
                    break  # Stop further checks if a duplicate is found

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        if instance and instance.pk:
            existing_article_ids = instance.detailcollection_set.values_list('article_id', flat=True)
            self.fields['articles'].queryset = Article.objects.exclude(id__in=existing_article_ids)
        else:
            self.fields['articles'].widget = forms.SelectMultiple(attrs={'size': 10})
            self.fields['articles'].queryset = Article.objects.all()


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    form = CollectionForm
    inlines = [DetailCollectionInline]
    list_display = ('libelle','disponible')
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {
            'fields': ('libelle', 'description', 'image', 'image_tag', 'disponible')
        }),
    )


@admin.register(Pierre)
class PierreAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag','cover_tag',)
    fieldsets = (
        (None, {
            'fields': ('libelle','description', 'image', 'image_tag', 'couverture', 'cover_tag')
        }),
    )


admin.site.register(TagBesoin)
admin.site.register(Categorie)
admin.site.register(SousCategorie)
@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'discount_percentage', 'end_date')

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
    

@admin.register(Voyance)
class VoyanceAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'type', 'tarif')
    readonly_fields = ('type',)
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    
@admin.register(VIPromo)
class VIPromoAdmin(admin.ModelAdmin):
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