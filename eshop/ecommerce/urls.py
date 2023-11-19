from django.urls import include, path
from .views import *

# router = routers.DefaultRouter()
# router.register(r'articles', ArticleViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

handler404 = 'ecommerce.views.erreur_view'
handler500 = 'ecommerce.views.erreur_view'
handler403 = 'ecommerce.views.erreur_view'
handler400 = 'ecommerce.views.erreur_view'

urlpatterns = [
    
    path('', accueil_view, name='accueil'),
    path('articles/', articles_view, name='articles'),
    path('inscription/', signup_view, name='inscription'),
    #path('connexion/', connexion_view, name='connexion'),
    path('mentions-legales/', mentions_view, name='mentions'),
    path('conditions-generales-de-vente/', conditions_view, name='conditions'),
    path('pierres-en-lithotherapie/', pierres_view, name='pierres'),
    path('erreur-404/', erreur_view, name='erreur404'),
    path('mot-de-passe-oublié/', resetpwrd_view, name='reset_password'),
    path('mon-panier/', panier_view, name='panier'),
    path('confirmation-de-commande/', checkout_view, name='checkout'),
    path('mon-profil/', profil_view, name='profil'),
    path('deconnexion/', logout_view, name='deconnexion'),
    path('connexion/', CustomLoginView.as_view(), name='connexion'),

    path('profil/update_personal_info/', update_personal_info, name='update_personal_info'),
    path('profil/update_password/', update_password, name='update_password'),
]