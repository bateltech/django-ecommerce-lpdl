from django.contrib import admin


from .models import Article, Commande, DetailCommande, Pierre, PrixArticle, TagBesoin, Categorie, SousCategorie, Commentaire, Feedback, ClientUser, Wishlist
from .models import Cart, CartItem, Newsletter


admin.site.register(ClientUser)

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', 'pierres')  # Display tags and pierres as checkboxes

admin.site.register(Article, ArticleAdmin)
admin.site.register(Pierre)
admin.site.register(TagBesoin)
admin.site.register(PrixArticle)
admin.site.register(Categorie)
admin.site.register(SousCategorie)


admin.site.register(Commande)
admin.site.register(DetailCommande)
# admin.site.register(Commentaire) # pour la version 2

admin.site.register(Feedback)
# admin.site.register(Newsletter)