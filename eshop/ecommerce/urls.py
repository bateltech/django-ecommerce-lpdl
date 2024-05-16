from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from .views import *
from django.views.generic.base import TemplateView  # new

# router = routers.DefaultRouter()
# router.register(r'articles', ArticleViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    
    path('accueil/', accueil_view, name='accueil'),
    path('articles/', articles_view, name='articles'),
    path('inscription/', signup_view, name='inscription'),
    path('mentions-legales/', mentions_view, name='mentions'),
    path('conditions-generales-de-vente/', conditions_view, name='conditions'),
    re_path(r'^pierres-en-lithotherapie/$', pierres_view, name='pierres'),
    path('erreur-404/', erreur_view, name='erreur404'),
    path('mot-de-passe-oublié/', resetpwrd_view, name='reset_password_process'),
    path('mon-panier/', panier_view, name='panier'),
    path('confirmation-de-commande-par-carte-bancaire/', checkout_view, name='checkout'),
    path('mon-profil/', profil_view, name='profil'),
    path('securite/', securite_view, name='securite'),
    path('mes-favoris/', favoris_view, name='favoris'),
    path('mes-commentaires/', commentaires_view, name='commentaires'),
    path('historique-des-achats/', historique_view, name='historique'),
    path('deconnexion/', logout_view, name='deconnexion'),
    path('connexion/', CustomLoginView.as_view(), name='connexion'),
    path('details/<int:article_id>/', details_view, name="details"),
    path('paiement-de-voyance/', paiement_voyance_view, name='paiement_voyance'),
    path('achat-effectué/', stripe_success, name='stripe_success'),
    path('accueil/achat-annulé', stripe_cancel, name='stripe_cancel'),
    path('paiement-effectué/', voyance_success, name='voyance_success'),
    #path('webhook/', stripe_webhook, name='webhook'),

    path('mon-profil/update_personal_info/', update_personal_info, name='update_personal_info'),
    path('mon-profil/update_password/', update_password, name='update_password'),
    path('add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('search/', search_results, name='search'),
    path('formulaire-de-voyance/', formulaire_voyance, name='formulaire_voyance'),
    # path('finaliser_commande/', finaliser_commande, name='finaliser_commande'),

    path('start_order/',start_order,name='start_order'),
    path('voyance_order/', voyance_order, name='voyance_order'),

    path('submit-feedback/', submit_feedback, name='submit_feedback'),

    path('reinitialisation-du-mot-de-passe/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('abonnement/', abonnement, name='abonnement'),
    path("newsletter/", newsletter, name="newsletter"),
    path("sendEmail/", sendEmail, name="sendEmail"),

    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    

]