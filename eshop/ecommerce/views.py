# views.py
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Commande, VIPromo, Promo, Collection, Pierre, Categorie, SousCategorie, Commentaire, TagBesoin, DetailCommande, PrixArticle, Article, Feedback, ClientUser, Wishlist, Voyance, Cart, CartItem, DemandeVoyance
from .serializers import CommandeSerializer, PierreSerializer, CategorieSerializer, SousCategorieSerializer, CommentaireSerializer, TagBesoinSerializer, DetailCommandeSerializer, PrixArticleSerializer, ArticleSerializer, FeedbackSerializer, UserSerializer, WishlistSerializer, CartSerializer, CartItemSerializer
from django.views.decorators.csrf import csrf_protect
from .forms import SignupForm, LoginForm, PersonalInfoForm, PasswordResetForm, VoyanceForm, NewsletterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout  # Importez les fonctions authenticate et login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone as time
from django.contrib import messages
from django.conf import settings


import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from sib_api_v3_sdk.api.lists_api import ListsApi
from datetime import datetime, timezone,timedelta
import pytz

# Vues des modèles

class UserViewSet(viewsets.ModelViewSet):
    queryset = ClientUser.objects.all()
    serializer_class = UserSerializer

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

class PierreViewSet(viewsets.ModelViewSet):
    queryset = Pierre.objects.all()
    serializer_class = PierreSerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class SousCategorieViewSet(viewsets.ModelViewSet):
    queryset = SousCategorie.objects.all()
    serializer_class = SousCategorieSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer

class TagBesoinViewSet(viewsets.ModelViewSet):
    queryset = TagBesoin.objects.all()
    serializer_class = TagBesoinSerializer

class DetailCommandeViewSet(viewsets.ModelViewSet):
    queryset = DetailCommande.objects.all()
    serializer_class = DetailCommandeSerializer

class PrixArticleViewSet(viewsets.ModelViewSet):
    queryset = PrixArticle.objects.all()
    serializer_class = PrixArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

# Vues des erreurs

def error_400(request, exception):
    return render(request, 'erreur.html', status=400)

def error_403(request, exception):
    return render(request, 'erreur.html', status=403)

def error_404(request, exception):
    return render(request, 'erreur.html', status=404)

def error_500(request):
    return render(request, 'erreur.html', status=500)



# Vues des fonctionnalités
    
def accueil_view(request):
    form = VoyanceForm()

    collections = Collection.objects.all()
    print("mes collections : ", collections.__len__())

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    
    vipromoobj = VIPromo.objects.filter(client=request.user).first() if utilisateur_connecte else None
    notvipromo = True
    if vipromoobj:
        notvipromo = False

    # Calculate the date one month ago from today
    one_month_ago = time.now() - timedelta(days=30)
    
    # Get all articles created at most one month from today
    recent_articles = Article.objects.filter(created_at__gte=one_month_ago)
    
    # Fetch all active promos
    active_promos = Promo.objects.filter(end_date__gte=time.now())

    # Fetch voyances
    voyances = Voyance.objects.all()

    print(notvipromo)
    context = {'utilisateur_connecte': utilisateur_connecte,
                'prenom_utilisateur': prenom_utilisateur,
                'form':form,
               'notvipromo': notvipromo,
               'recent_articles': recent_articles,
               'recent_articles_count': recent_articles.count(),
               'active_promos': active_promos,
               'collections': collections,
               'voyances': voyances,
               }
    
    return render(request, 'accueil.html', context)


def articles_view(request):
    categories = Categorie.objects.all()
    sub_categories = SousCategorie.objects.filter(categorie__in=categories)
    articles = Article.objects.filter(sous_categorie__in=sub_categories)
    # print("Categories:", categories)
    print("Subcategories:", sub_categories)


    # Fetch all active promos
    active_promos = Promo.objects.filter(end_date__gte=time.now())
    print("promos : ", active_promos.__len__())


    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

    wishlist_article_ids = []  # Liste pour stocker les IDs des articles dans la wishlist de l'utilisateur connecté
    
    if utilisateur_connecte:

        # Récupérer la wishlist de l'utilisateur connecté s'il est connecté
        wishlist = Wishlist.objects.filter(client=request.user.id)
        if wishlist.exists():  # Vérifier si la wishlist existe pour cet utilisateur
            # Extraire les IDs des articles dans la wishlist
            wishlist_article_ids = list(wishlist.values_list('articles', flat=True))


    context = {'utilisateur_connecte': utilisateur_connecte,
                'prenom_utilisateur': prenom_utilisateur,
                'sub_categories': sub_categories,
                'articles': articles,
                'categories': categories,
                'wishlist_article_ids': wishlist_article_ids,
                'active_promos': active_promos  # Pass active promos for each article to the template
                }
    
    return render(request, 'articles.html', context)

def details_view(request, article_id):
    article = Article.objects.get(pk=article_id)
    price = article.prix_article.all()
    categories = Categorie.objects.all()
    similar_articles = Article.objects.filter(categorie=article.categorie, sous_categorie=article.sous_categorie).exclude(pk=article_id)

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

    # Fetch all active promos
    active_promos = Promo.objects.filter(end_date__gte=time.now(), articles=article)

    if utilisateur_connecte:
        favoris = Wishlist.objects.filter(client=request.user).exists()
        if favoris:
            wishlist_articles = Wishlist.objects.get(client=request.user).articles.all()
            favoris = article in wishlist_articles
        else:
            favoris = False
    else:
        favoris = False

    context = {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur': prenom_utilisateur,
        'article': article,
        'prices': price,
        'price': price.first(),
        'categories': categories,
        'similar_articles': similar_articles,
        'active_promos': active_promos,
        'favoris': favoris }
    return render(request, 'details.html', context)


def detailscollect_view(request, collection_id):
    
    collection = Collection.objects.get(pk=collection_id)

    print("collection id  : ", collection_id)

    # Fetch all active promos
    active_promos = Promo.objects.filter(end_date__gte=time.now())


    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

    wishlist_article_ids = []  # Liste pour stocker les IDs des articles dans la wishlist de l'utilisateur connecté
    
    if utilisateur_connecte:

        # Récupérer la wishlist de l'utilisateur connecté s'il est connecté
        wishlist = Wishlist.objects.filter(client=request.user.id)
        if wishlist.exists():  # Vérifier si la wishlist existe pour cet utilisateur
            # Extraire les IDs des articles dans la wishlist
            wishlist_article_ids = list(wishlist.values_list('articles', flat=True))


    context = {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur': prenom_utilisateur,
        'collection': collection,
        'wishlist_article_ids': wishlist_article_ids,
        'active_promos': active_promos }
    return render(request, 'details_collection.html', context)


def mentions_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'mentions.html', context)

def connexion_view(request):
    return render(request, 'connexion.html')

def conditions_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'conditions.html', context)


from django.shortcuts import get_object_or_404

def pierres_view(request):
    pierres = Pierre.objects.all()
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

    # Récupérez les paramètres d'URL
    libelle = request.GET.get('pierre', None)
    pierre_id = request.GET.get('id', None)

    print("la pierre ", libelle)

    if libelle and pierre_id:
        # Sélectionnez la pierre correspondante
        selected_pierre = get_object_or_404(Pierre, id=pierre_id)
    else:
        # Par défaut, sélectionnez la première pierre
        selected_pierre = pierres.first()

    print("la pierre selectionnée ", selected_pierre.libelle)
    context = {'pierres': pierres, 'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'selected_pierre': selected_pierre}
    return render(request, 'pierres.html', context)

def erreur_view(request, exception=None):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'erreur.html', context)

def resetpwrd_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'resetpwrd.html', context)

@login_required()
def panier_view(request):
    # Retrieve the current user
    user = request.user
    
    # Check if the user has a cart
    has_cart = CartItem.objects.filter(cart__user=user).exists()
    cart_items = CartItem.objects.filter(cart__user=user)
    # Retrieve feedback data
    feedback_items = Feedback.objects.filter(etat='publie')

    total_price = sum(item.item_price * item.quantity  for item in cart_items)
    print("total price in panier : ", total_price)

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    nom_utiisateur = request.user.last_name if utilisateur_connecte else None
    email_utilisateur = request.user.email if utilisateur_connecte else None
    context = {
            'utilisateur_connecte': utilisateur_connecte,
            'prenom_utilisateur': prenom_utilisateur,
            'has_cart': has_cart,
            'cart_items': cart_items,
            'nom_utilisateur': nom_utiisateur,
            'email_utilisateur': email_utilisateur,
            'feedback_items': feedback_items,
            'total_price' : total_price
        }
    
    return render(request, 'panier.html', context)


import datetime
from decimal import Decimal, ROUND_HALF_UP

@login_required() 
def checkout_view(request):
    user = request.user

    utilisateur_connecte =  request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    nom_utilisateur = request.user.last_name if utilisateur_connecte else None
    email_utilisateur = request.user.email if utilisateur_connecte else None

    vip = False

    # Check if the user has a cart
    has_cart = CartItem.objects.filter(cart__user=user).exists()

    total_price = 0
    if has_cart:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart__user=user)
        print("cart price : ", cart.total_price)

        price_promo = cart.total_price
        
        # Apply VIPromo discount if applicable
        vipromo = VIPromo.objects.filter(client=user).first()
        if vipromo and vipromo.end_date >= datetime.datetime.now().date():
            discount_percentage = Decimal(vipromo.discount_percentage) / 100
            print(" price before :", price_promo)
            price_promo *= (1 - discount_percentage)
            price_promo = price_promo.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            price_promo += 5
            print("promo : ", discount_percentage)
            print(" promo price :", price_promo)
            vip = True


        total_price = cart.total_price + 5

    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    context= {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur' : prenom_utilisateur,
        'nom_utilisateur' : nom_utilisateur,
        'email_utilisateur' : email_utilisateur,
        'cart_items': cart_items,
        'has_cart': has_cart,
        'total_price' : total_price,
        'price_promo' : price_promo,
        'pub_key' : pub_key,
        'vip' : vip

    }

    return render(request, 'checkout.html', context)



@login_required()  # A CHERCHER COMMENT L'UTILISER
def profil_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    
    form = PersonalInfoForm(instance=request.user)

    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'user': utilisateur, 'form': form}
    return render(request, 'profil.html', context)

@login_required()  # A CHERCHER COMMENT L'UTILISER
def securite_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None

    form = PasswordResetForm(request.user)

    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'user': utilisateur, 'form': form}
    return render(request, 'securite.html', context)

@login_required()  # A CHERCHER COMMENT L'UTILISER
def favoris_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    
    if utilisateur_connecte:
        # Récupérer la wishlist de l'utilisateur connecté s'il est connecté
        try:
            wishlist = Wishlist.objects.get(client=request.user)
            articles_wishlist = wishlist.articles.all()
        except Wishlist.DoesNotExist:
            # Si l'utilisateur n'a pas de wishlist, initialiser une liste vide
            articles_wishlist = []
    else:
        articles_wishlist = []

    context = {'utilisateur_connecte': utilisateur_connecte,
               'prenom_utilisateur': prenom_utilisateur,
               'user': utilisateur,
                'articles': articles_wishlist }
    
    return render(request, 'favoris.html', context)

@login_required()  # A CHERCHER COMMENT L'UTILISER
def commentaires_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None

    feedbacks = Feedback.objects.filter(utilisateur=request.user)
    
    context = {
        'feedbacks': feedbacks,
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur': prenom_utilisateur,
        'user': utilisateur }
    
    return render(request, 'commentaires.html', context)

@login_required()  # A CHERCHER COMMENT L'UTILISER
def historique_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None

    commandes = Commande.objects.filter(user=request.user, etat='payee').order_by('-created_at')
    
    context = {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur': prenom_utilisateur,
        'commandes': commandes,
        'user': utilisateur }
    
    return render(request, 'historique.html', context)

from django.db import IntegrityError

@csrf_protect
def signup_view(response):
    if response.method == "POST":
        form = SignupForm(response.POST)
        if form.is_valid():
                try:
                    print("HURRAAAAY SUCCESS")
                    user = form.save()
                    login(response, user)  # Log in the user after registration
                    return redirect('accueil')  

                except IntegrityError as e:
                    print("OUPS !")
                    
                    # Gérer le cas où l'email existe déjà
                    form.add_error('email', 'Cet email est déjà utilisé.')
                    
                    return render(response, "inscription.html", {"form":form, "error_message":"Cet email est déjà utilisé. Veuillez choisir un autre email."})

        else: 
            print("failed to register")
            return render(response, "inscription.html", {"form":form})
                    
    else:
            form = SignupForm()

    return render(response, "inscription.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('connexion'))

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'connexion.html'  # Specify your login template
    form_class = LoginForm
    success_url = reverse_lazy('accueil')  # Replace 'home' with the actual name or path of your home page

@login_required
def update_personal_info(request):

    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            # Save the form data
            form.save()

            print("HURRAAAAAAAAAAAAAAAAAY")
            
            # Redirect or add success message
            messages.success(request, 'Informations personnelles mises à jour avec succès.')
            request.session['update_success'] = True  # Stockez un indicateur de succès dans la session
            return redirect('update_personal_info')
        else:
            print("que pd")
            print(request.user.phone_number)
            print(form.errors)
            # Error message
            messages.error(request, 'Erreur lors de la mise à jour des informations personnelles. Veuillez corriger les erreurs ci-dessous.')
            # Print form errors to console (for debugging)
            print("Error in form submission:", form.errors)
            return redirect('update_personal_info')
    else:
        form = PersonalInfoForm(instance=request.user)  # Replace with your user object

    return redirect('profil')

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            request.session['update_success'] = True  # Stockez un indicateur de succès dans la session
            return redirect('update_password')
        else:
            print("que pd")
            print(form.errors)

            messages.error(request, 'Les deux champs du nouveau mot de passe ne correspondent pas')
            # Print form errors to console (for debugging)
            print("Error in form submission:", form.errors)
            return redirect('update_password')
    else:
        form = PasswordChangeForm(request.user)
    
    return redirect('securite')

@login_required
def add_to_wishlist(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        # Check if the user has a wishlist
        try:
            wishlist = Wishlist.objects.get(client=request.user)
        except Wishlist.DoesNotExist:
            # If the user doesn't have a wishlist, create one
            wishlist = Wishlist.objects.create(client=request.user)
        
        # get article
        article = Article.objects.get(pk=article_id)

        # Add the article to the wishlist
        if wishlist.articles.filter(pk=article_id).exists():
            wishlist.articles.remove(article)
            added = False
        else:
            wishlist.articles.add(article)
            added = True
        
        # Return JSON response
        return JsonResponse({'added': added})
    
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        price_id = request.POST.get('price_id')
        # get article
        article = Article.objects.get(pk=article_id)
        price = PrixArticle.objects.get(pk=price_id)

         # Check for active promos for the article
        active_promos = Promo.objects.filter(end_date__gte=time.now(), articles=article)
        if active_promos.exists():
            promo = active_promos.first()
            discount = Decimal(promo.discount_percentage)
            print("discount", discount)
            discounted_price = price.prix * (1 - discount / 100)
        else:
            discounted_price = price.prix

        print("discounted count ", discounted_price)

        # Vérifier le stock de l'article
        if article.stock > 0:
            # Check if the user has a cart
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                # If the user doesn't have a cart, create one
                cart = Cart.objects.create(user=request.user)

            cart.save()

            # Create cart item
            try:    
                item = CartItem.objects.get(cart=cart, article=article, article_price=price)
                item.quantity = item.quantity + 1
                item.item_price = discounted_price
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(
                cart=cart,
                article=article,
                article_price=price,
                item_price = discounted_price)

            
            print("item price avant: ", item.item_price)
            item.save()
            print("item price : ", item.item_price)
            # cart.total_price = cart.total_price + price.prix
            cart.total_price = cart.total_price + discounted_price
            print("add to cart | new cart price : ", cart.total_price)
            cart.save()

            added_p = True
        else:
            added_p = False

        # Return JSON response
        return JsonResponse({'added_p': added_p})

from django.core.serializers.json import DjangoJSONEncoder
def search_results(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        article =request.POST.get('article')
        query_ar = Article.objects.filter(libelle__icontains=article)
        if len(query_ar)>0 and len(article)>0:
            data=[]
            for pos in query_ar:
                item={
                    'id':pos.id,
                    'name':pos.libelle,
                    'description':pos.description,
                    'image':pos.image.url if pos.image else None,

                }
                data.append(item)

            return JsonResponse({'data': data}, encoder=DjangoJSONEncoder)  # Use Django's JSON encoder
        else:
            return JsonResponse({'data': 'Aucun résultat...'})

    return JsonResponse({})

def formulaire_voyance(request):
    print(request.method)
    if request.method == 'POST':
        form = VoyanceForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data
            form.save()

            print("HURRAAAAAAAAAAAAAAAAAY")
        
            # Redirection vers la page de paiement
            return redirect('paiement_voyance')  # Assurez-vous d'avoir une URL nommée 'page_paiement' dans urls.py
        else: 
            print(form.errors)
            print("WHY GOD WHY GOD WHYYYYYYYY")
            return redirect('accueil')
    else:
        form = VoyanceForm(request.user)
        print("ARE YOU KIDDING ME ???")

    return render(request, 'accueil', {'form': form})

#@login_required
def abonnement(request):
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        email = request.POST.get('email')
        print(email)
        if email:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.SMTP_API_KEY
            print(configuration.api_key['api-key'])
            api_instance = ListsApi(sib_api_v3_sdk.ApiClient(configuration))
            api_instance2 = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
            list_id = 2
            api_response = api_instance.get_contacts_from_list(list_id)
            pprint(api_response)

            # check if the email already exists in the contact list
            for contact in api_response.contacts:
                if contact['email'] == email:
                    print("Im in !")
                    # Set VIP status to True for the user
                    try:
                        user = ClientUser.objects.get(email=email)
                        user.VIP = True
                        user.save()
                    except ClientUser.DoesNotExist:
                        pass

                    # Check if the user already has a VIPromo object
                    if not VIPromo.objects.filter(client=user).exists():
                        # If not, create a new one
                        start_date = datetime.datetime.now()
                        end_date = start_date + timedelta(days=365)  # 1 year from the start date
                        vipromo = VIPromo.objects.create(client=user, start_date=start_date, end_date=end_date)
                        print("vipromo created !")

                    return JsonResponse({'message': 'Déja abonné !'}, status=200)

            create_contact = sib_api_v3_sdk.CreateContact(email=email, list_ids=[list_id])
            api_response2 = api_instance2.create_contact(create_contact)
            
            # Set VIP status to True for the user
            try:
                user = ClientUser.objects.get(email=email)
                user.VIP = True
                user.save()

                # Create VIPromo object for the user
                start_date = datetime.datetime.now()
                end_date = start_date + timedelta(days=365)  # 1 year from the start date
                vipromo = VIPromo.objects.create(client=user, start_date=start_date, end_date=end_date)
                print("new vipromo created !")

            except ClientUser.DoesNotExist:
                pass

            return JsonResponse({'message': 'Abonnement effectué !'}, status=200)
    
    return JsonResponse({'message': 'Bad request'}, status=400)


# NOT USED FOR NOW
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():

            # Your email sending logic here
            return redirect('newsletter')  # Redirect after successfully sending the email
    else:
        form = NewsletterForm()

    return render(request, 'newsletter.html', {'form': form})

def sendEmail(sujet, contenu):

    try:
        subject = sujet
        # content = {"params": {"content": contenu}}

        content = contenu
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] =  settings.SMTP_API_KEY
        api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
        sender = {"name": 'La pierre de lune', "email": 'medjaoui.imene@gmail.com'}
        name = subject
        subject = subject
        recipients = {"listIds": [2]}
        scheduled_at = (datetime.now(pytz.utc) + timedelta(minutes=1)).isoformat()
        unsubscribe_id = '65fd9b792c61483dba7e8b8e'
        email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(scheduled_at =scheduled_at ,sender=sender, name=name,  subject=subject,  recipients=recipients, html_content=content, unsubscription_page_id=unsubscribe_id, inline_image_activation=True) # CreateEmailCampaign | Values to create a campaign

        api_response = api_instance.create_email_campaign(email_campaigns)
        pprint(api_response)
        print(content)
        print('newsletter sent successfully !')
        return JsonResponse({'success': True, 'message': 'Quantity updated successfully' })
    except Exception as e:
        # Log other exceptions
        print(f'Error sending newsletter: {e}')
        return JsonResponse({'success': False, 'message': 'An error occurred during newsletter sending'})

@require_POST
@csrf_protect
def update_quantity_ajax(request, item_id, new_quantity):
    try:
        # Perform the lookup for the cart item
        cart_item = CartItem.objects.get(id=item_id)

        # Get the cart associated with the cart item
        cart = cart_item.cart

        # Update the quantity
        cart_item.quantity = new_quantity
        cart_item.save()

        # Recalculate the total price of the cart
        cart.calculate_total_price()
        print("update_quantity_ajax | cart total price : ", cart.total_price)
        cart.save()

        return JsonResponse({'success': True, 'message': 'Quantity updated successfully' })
    except CartItem.DoesNotExist:
        # Log the error and return a response
        print(f'Error: Cart item with id {item_id} not found.')
        return JsonResponse({'success': False, 'message': 'Cart item not found'})
    except Exception as e:
        # Log other exceptions
        print(f'Error updating quantity: {e}')
        return JsonResponse({'success': False, 'message': 'An error occurred during quantity update'})

from django.db.models import Sum

def get_item_price(request, item_id):
    try:
        # Fetch the CartItem object based on item_id
        cart_item = CartItem.objects.get(pk=item_id)
        item_price = cart_item.item_price
        total_item_price = cart_item.total_item_price
        cart = cart_item.cart

        # # Calculate the total price of the cart
        # total_price = cart.cartitem_set.aggregate(total=Sum('total_item_price'))['total']
        total_price = cart.total_price
        print("get item price | cart total price : ",total_price)

        # Return the item price and total price as JSON response
        return JsonResponse({'item_price': item_price, 'total_item_price': total_item_price, 'total_price': total_price})
    except CartItem.DoesNotExist:
        # Handle the case where CartItem with given item_id does not exist
        return JsonResponse({'error': 'CartItem not found'}, status=404)
    except Exception as e:
        # Handle any other exceptions
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
@csrf_protect
def delete_Cart_item_ajax (request, item_id):
    try:
        # Retrieve the CartItem instance
        cart_item = CartItem.objects.get(pk=item_id)

        total_item_price = cart_item.total_item_price
        cart = cart_item.cart
        cart.total_price = cart.total_price - cart_item.total_item_price
        cart.save()
        # Delete the Item
        cart_item.delete()

        return JsonResponse({'success': True, 'message': 'Item successfully deleted', 'total_item_price': total_item_price})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@require_POST
@csrf_protect
def delete_Voyance_ajax (request, item_id):
    try:
        # Retrieve the Voyance instance
        voyance = Voyance.objects.get(pk=item_id)

        # Delete the Item
        voyance.delete()

        return JsonResponse({'success': True, 'message': 'Item successfully deleted'})
    except Voyance.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

from datetime import datetime, timezone
def submit_feedback(request):
    if request.method == 'POST':
        contenu = request.POST.get('contenu')

        user_id = request.user.id if request.user.is_authenticated else None

        # Create a Feedback object and save it to the database
        feedback = Feedback(
            contenu=contenu,
            date_envoi=datetime.now(timezone.utc),
            utilisateur_id=user_id,
            etat='en attente'
        )
        feedback.save()

        messages.success(request, 'Feedback submitted successfully!')
        return redirect('panier')  # Redirect to a success page or another URL
    else:
        # Handle non-POST requests as needed
        return render(request, 'accueil.html')
 

import json
import stripe
from django.http import JsonResponse
from .models import Cart, CartItem, Commande, DetailCommande

from decimal import Decimal, ROUND_HALF_UP
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import stripe
from django.conf import settings
import json
from .models import Cart, CartItem, Commande, DetailCommande, VIPromo
from django.urls import reverse
import datetime

@csrf_protect
@login_required
def start_order(request):
    cart = Cart.objects.get(user=request.user)
    data = json.loads(request.body)

    items = []
    total_price = Decimal(cart.total_price)
    print("start order | total prix : ", total_price)

    cartItems = CartItem.objects.filter(cart=cart)

    # Prepare items list and calculate initial total price
    for item in cartItems:
        product = item.article
        print("prix in for loop : ", item.item_price)

        items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': product.libelle,
                },
                'unit_amount': int(item.item_price * 100),  # Stripe expects amounts in cents
            },
            'quantity': item.quantity
        })

    stripe.api_key = settings.STRIPE_API_SECRET_KEY

    # Retrieve the delivery fee item from Stripe
    delivery_fee_item = stripe.ShippingRate.retrieve('shr_1PEGGcHwNiNEPJKYCIwfx5o3')

    if total_price < 65:
        # Add the delivery fee item to the items list
        items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Frais de livraison',
                },
                'unit_amount': int(delivery_fee_item.fixed_amount.amount),
            },
            'quantity': 1,
        })
        total_price += Decimal(delivery_fee_item.fixed_amount.amount) / 100

    # Apply VIPromo discount if applicable
    vipromo = VIPromo.objects.filter(client=request.user).first()
    if vipromo and vipromo.end_date >= datetime.datetime.now().date():
        discount_percentage = Decimal(vipromo.discount_percentage) / 100
        print("discount percentage:", discount_percentage)
        total_discount = (total_price - Decimal(delivery_fee_item.fixed_amount.amount) / 100 ) * discount_percentage
        print("total discount:", total_discount)

        # Recalculate total_price after applying the discount
        total_price_after_discount = total_price - total_discount
        print("total price after discount:", total_price_after_discount)

        # Apply the discount to the session creation for Stripe
        session_total_price = total_price_after_discount

        # Since we cannot directly modify delivery fee in Stripe session, adjust only product items
        discount_per_item = total_discount / sum(item.quantity for item in cartItems)
        discount_per_item = discount_per_item.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        for item in items:
            if item['price_data']['product_data']['name'] != 'Frais de livraison':
                item_total_price = Decimal(item['price_data']['unit_amount']) / 100  # Convert from cents to euros
                item_total_price_after_discount = item_total_price - discount_per_item
                item['price_data']['unit_amount'] = int(item_total_price_after_discount * 100)  # Convert back to cents

    success_url = request.build_absolute_uri(reverse('stripe_success')) + '?session_id={CHECKOUT_SESSION_ID}'
    cancel_url = request.build_absolute_uri(reverse('stripe_cancel'))

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'paypal'],
        line_items=items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url
    )

    payment_intent = session.payment_intent
    print("payment intent in checkout:", session.payment_intent)
    print("session id in checkout:", session.id)

    commande = Commande.objects.create(
        user=request.user,
        prenom=data['prenom'],
        nom=data['nom'],
        email=data['email'],
        telephone=data['telephone'],
        adresse=data['adresse'],
        numero_rue=data['numero_rue'],
        code_postal=data['code_postal'],
        ville=data['ville'],
        etat='en attente',
        total_price=total_price_after_discount,
        session_id=session.id,
        payment_intent=payment_intent
    )

    for item in cartItems:
        product = item.article
        quantity = item.quantity
        prix_article = item.article_price
        print("prix par item:", item.item_price)
        print("taille par item:", prix_article.taille)

        detail_commande = DetailCommande.objects.create(
            commande=commande,
            article=product,
            item_price=item.item_price,
            quantity=quantity,
            size=prix_article.taille if prix_article.type_prix == 'size_based' else None
        )
        detail_commande.save()

    print("recalculate in start order | total price:", commande.total_price)

    commande.save()
    print("Session ID in start order:", session.id)
    return JsonResponse({'session': session, 'commande': payment_intent, 'sessionId': session.id})


import stripe
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@login_required() 
@csrf_exempt
def stripe_success(request):
    session_id = request.GET.get('session_id')
    print ("session id : ", session_id)
    if session_id:
        stripe.api_key = settings.STRIPE_API_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        print("payment status : ", session.payment_status)
        if session.payment_status == 'paid':
            # Retrieve the corresponding Commande object
            commande = Commande.objects.get(session_id=session.id)

            commande.etat = 'payee' # Update etat to "payee"
            commande.payment_intent = session.payment_intent
            print('payment intent after success : ', session.payment_intent)
            commande.save()

            cart = Cart.objects.get(user=commande.user)

            for item in cart.cartitem_set.all():
                product = item.article
                quantity = item.quantity
                # Update the product quantity
                product.stock -= quantity
                product.save()

            # Empty the cart
            cart.cartitem_set.all().delete()
            cart.delete()

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'stripe_success.html', context)


def stripe_cancel(request):
    session_id = request.GET.get('session_id')
    try:
        commandes = Commande.objects.filter(user=request.user, etat='en attente')
        for commande in commandes:
            commande.delete()
    except Commande.DoesNotExist:
        pass
    
    collections = Collection.objects.all()
    print("mes collections : ", collections.__len__())

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    
    vipromoobj = VIPromo.objects.filter(client=request.user).first() if utilisateur_connecte else None
    notvipromo = True
    if vipromoobj:
        notvipromo = False

    # Calculate the date one month ago from today
    one_month_ago = time.now() - timedelta(days=30)
    
    # Get all articles created at most one month from today
    recent_articles = Article.objects.filter(created_at__gte=one_month_ago)
    
    # Fetch all active promos
    active_promos = Promo.objects.filter(end_date__gte=time.now())

    # Fetch voyances
    voyances = Voyance.objects.all()

    print(notvipromo)
    context = {'utilisateur_connecte': utilisateur_connecte,
               'prenom_utilisateur': prenom_utilisateur,
               'notvipromo': notvipromo,
               'recent_articles': recent_articles,
               'recent_articles_count': recent_articles.count(),
               'active_promos': active_promos,
               'collections': collections,
               'voyances': voyances,
               }

    # ... handle cancelled payment ...
    return render(request, 'accueil.html', context)



# # TODO : READ WEBHOOKS DOCS & WATCH TUTORIALS
# @csrf_exempt
# def stripe_webhook(request):
#     payload = json.loads(request.body)
#     event_type = payload['type']

#     if event_type == 'checkout.session.completed':
#         session = stripe.checkout.Session.retrieve(payload['data']['object']['id'])
#         payment_intent = session.payment_intent

#         # Retrieve the corresponding Commande object
#         commande = Commande.objects.get(payment_intent=payment_intent)

#         if payment_intent is not None and payment_intent.status == 'succeeded':
#             commande.etat = 'payee' # Update etat to "payee"
#             commande.save()

#             cart = Cart.objects.get(user=commande.user)

#             for item in cart.cartitem_set.all():
#                 product = item.article
#                 quantity = item.quantity
#                 # Update the product quantity
#                 product.stock -= quantity
#                 product.save()

#             # Empty the cart
#             cart.cartitem_set.all().delete()

#     return JsonResponse({'status': 'success'})


@login_required()
def choose_voyance_view(request, voyance_id):
    # Retrieve the selected voyance
    print("error ?")
    voyance = get_object_or_404(Voyance, id=voyance_id)

    print('voyance : ', voyance.libelle)

    # Create a new DemandeVoyance object
    demande_voyance = DemandeVoyance.objects.create(
        user=request.user,
        total_price=voyance.tarif,
        telephone=request.user.phone_number,  # You may need to adjust this
        nom=request.user.last_name,  # You may need to adjust this
        prenom=request.user.first_name,  # You may need to adjust this
        email=request.user.email,
        voyance=voyance.libelle,
        type=voyance.type,
        etat='en attente'
    )


    print("demande_voyance : ", demande_voyance.id)

    # Redirect to the payment view with the new DemandeVoyance object
    return redirect('paiement_voyance', demande_voyance_id=demande_voyance.id)

@login_required()
def paiement_voyance_view(request, demande_voyance_id):
    # Retrieve the current user
    user_v = request.user
    
    # Retrieve the DemandeVoyance object

    demande_voyance = get_object_or_404(DemandeVoyance, id=demande_voyance_id)
    print("demande de voyance : ", demande_voyance.etat)
    
    # Retrieve the Voyance description
    description = Voyance.objects.filter(type=demande_voyance.type).first().description

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    context = { 'pub_key': pub_key,
            'utilisateur_connecte': utilisateur_connecte,
            'prenom_utilisateur': prenom_utilisateur,
            'cart_items': demande_voyance,
            'description': description,
            'total_price' : demande_voyance.total_price,
        }
    
    return render(request, 'paiement_voyance.html', context)

@csrf_protect
@login_required
def voyance_order(request, demande_voyance_id):

    data = json.loads(request.body)

    print("in voyance order baby yeah !")

    demande_voyance = get_object_or_404(DemandeVoyance, id=demande_voyance_id)
    
    demande_voyance.prenom=data['prenom']
    demande_voyance.nom=data['nom']
    demande_voyance.email=data['email']
    demande_voyance.telephone=data['telephone']
    total_price = demande_voyance.total_price
    voyance = demande_voyance.voyance

    unit_amount = int(total_price * 100)

    stripe.api_key = settings.STRIPE_API_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'paypal'],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": voyance,
                },
                "unit_amount": unit_amount,
            },
            "quantity": 1,
        }],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('voyance_success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= request.build_absolute_uri(reverse('voyance_cancel'))
    )

    # Confirm the payment intent
    # stripe.PaymentIntent.confirm(session.payment_intent, payment_method=data['payment_method'])

    
    demande_voyance.session_id= session.id
    demande_voyance.payment_intent=session.payment_intent

    demande_voyance.save()

    return JsonResponse({'session': session, 'voyance': session.payment_intent})


@login_required() 
@csrf_exempt
def voyance_success(request):
    session_id = request.GET.get('session_id')
    print ("session id : ", session_id)
    if session_id:
        stripe.api_key = settings.STRIPE_API_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        print("voyance payment status : ", session.payment_status)
        if session.payment_status == 'paid':
            # Retrieve the corresponding Commande object
            commande = DemandeVoyance.objects.get(session_id=session.id)

            commande.etat = 'payee' # Update etat to "payee"
            commande.payment_intent = session.payment_intent
            print('payment intent after success : ', session.payment_intent)
            commande.save()

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'stripe_success.html', context)

@login_required() 
@csrf_exempt
def voyance_cancel(request):
    session_id = request.GET.get('session_id')
    try:
        commandes = DemandeVoyance.objects.filter(user=request.user, etat='en attente')
        for commande in commandes:
            commande.delete()
    except DemandeVoyance.DoesNotExist:
        pass
    
    collections = Collection.objects.all()
    print("mes collections : ", collections.__len__())

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    
    vipromoobj = VIPromo.objects.filter(client=request.user).first() if utilisateur_connecte else None
    notvipromo = True
    if vipromoobj:
        notvipromo = False

    # Calculate the date one month ago from today
    one_month_ago = time.now() - timedelta(days=30)
    
    # Get all articles created at most one month from today
    recent_articles = Article.objects.filter(created_at__gte=one_month_ago)
    
    # Fetch all active promos
    active_promos = Promo.objects.filter(end_date__gte=time.now())

    # Fetch voyances
    voyances = Voyance.objects.all()

    print(notvipromo)
    context = {'utilisateur_connecte': utilisateur_connecte,
               'prenom_utilisateur': prenom_utilisateur,
               'notvipromo': notvipromo,
               'recent_articles': recent_articles,
               'recent_articles_count': recent_articles.count(),
               'active_promos': active_promos,
               'collections': collections,
               'voyances': voyances,
               }

    # ... handle cancelled payment ...
    return render(request, 'accueil.html', context)
