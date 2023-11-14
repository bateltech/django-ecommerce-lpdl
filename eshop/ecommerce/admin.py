from django.contrib import admin


from .models import Article, Commande, DetailCommande, Pierre, PrixArticle, TagBesoin, Categorie, SousCategorie, Commentaire, Feedback, ClientUser, Wishlist
from .models import Cart, CartItem


admin.site.register(ClientUser)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)


admin.site.register(Article)
admin.site.register(Pierre)
admin.site.register(TagBesoin)
admin.site.register(PrixArticle)
admin.site.register(Categorie)
admin.site.register(SousCategorie)


admin.site.register(Commande)
admin.site.register(DetailCommande)
admin.site.register(Commentaire)
admin.site.register(Feedback)