# views.py
from django.http import HttpResponse
from rest_framework import viewsets
from .models import TailleArticle, Commande, Pierre, Categorie, SousCategorie, Commentaire, TagBesoin, DetailCommande, PrixArticle, Article, Feedback, ClientUser, Wishlist, Voyance, Cart, CartItem
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
from django.utils import timezone
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

class TailleArticleViewSet(viewsets.ModelViewSet):
    queryset = TailleArticle.objects.all()
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
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    return render(request, 'accueil.html', {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'form':form})

def articles_view(request):
    categories = Categorie.objects.all()
    sub_categories = SousCategorie.objects.filter(categorie__in=categories)
    articles = Article.objects.filter(sous_categorie__in=sub_categories)
    # print("Categories:", categories)
    print("Subcategories:", sub_categories)
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
                'wishlist_article_ids': wishlist_article_ids }
    return render(request, 'articles.html', context)

def details_view(request, article_id):
    article = Article.objects.get(pk=article_id)
    price = article.prix_article.all()
    categories = Categorie.objects.all()
    similar_articles = Article.objects.filter(categorie=article.categorie, sous_categorie=article.sous_categorie).exclude(pk=article_id)

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

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
        'favoris': favoris }
    return render(request, 'details.html', context)


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


def paiement_voyance_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'paiement_voyance.html', context)

@login_required()
def paiement_voyance_view(request):
    # Retrieve the current user
    user_v = request.user
    
    cart_items = Voyance.objects.filter(email=user_v.email, etat="en attente")
    

    total_price = sum(item.tarif for item in cart_items)

    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None

    context = {
            'utilisateur_connecte': utilisateur_connecte,
            'prenom_utilisateur': prenom_utilisateur,
            'cart_items': cart_items,
            'total_price' : total_price
        }
    
    return render(request, 'paiement_voyance.html', context)



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
    feedback_items = Feedback.objects.filter(etat=1)

    total_price = sum(item.item_price for item in cart_items)

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

@login_required() 
def checkout_view(request):
    user = request.user

    utilisateur_connecte =  request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    nom_utilisateur = request.user.last_name if utilisateur_connecte else None
    email_utilisateur = request.user.email if utilisateur_connecte else None

    # Check if the user has a cart
    has_cart = CartItem.objects.filter(cart__user=user).exists()

    total_price =0
    if has_cart:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart__user=user)
        total_price = cart.total_price

    context= {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur' : prenom_utilisateur,
        'nom_utilisateur' : nom_utilisateur,
        'email_utilisateur' : email_utilisateur,
        'cart_items': cart_items,
        'has_cart': has_cart,
        'total_price' : total_price
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
    
    context = {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur': prenom_utilisateur,
        'user': utilisateur }
    
    return render(request, 'commentaires.html', context)


@login_required()  # A CHERCHER COMMENT L'UTILISER
def historique_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    
    context = {
        'utilisateur_connecte': utilisateur_connecte,
        'prenom_utilisateur': prenom_utilisateur,
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
                    print("MOTHER FUCKER => ", form.errors)
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
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(
                cart=cart,
                article=article,
                article_price=price)

            item.save()

            cart.total_price = cart.total_price + price.prix
            cart.save()

            # Décrémenter le stock de l'article
            article.stock -= 1
            article.save()

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
        print("ARE YOU FUCKING KIDDING ME ???")

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
                    return JsonResponse({'message': 'Déja abonné !'}, status=200)

            create_contact = sib_api_v3_sdk.CreateContact(email=email, list_ids=[list_id])
            api_response2 = api_instance2.create_contact(create_contact)
            return JsonResponse({'message': 'Abonnement effectué !'}, status=200)
    
    return JsonResponse({'message': 'Bad request KHRA'}, status=400)


def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():

            # Your email sending logic here
            return redirect('newsletter')  # Redirect after successfully sending the email
    else:
        form = NewsletterForm()

    return render(request, 'newsletter.html', {'form': form})


# def sendEmail(request):
#     if(request.method=='POST'):
#        form = NewsletterForm(request.POST)
#        if form.is_valid():
#             subject = form.cleaned_data.get('subject')
#             content= form.cleaned_data.get('message')
#             #content= 'ROH TKHRA YA CKEDITOR TA3 LA MERDE REERJEORJEOFJEFJOFJEOFJZF FJERFOIJEROIJEROJERO FRJEIRFJEIROJ EZROI'
#             configuration = sib_api_v3_sdk.Configuration()
#             configuration.api_key['api-key'] =  settings.SMTP_API_KEY
#             api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
#             sender = {"name": 'La pierre de lune', "email": 'medjaoui.imene@gmail.com'}
#             name = subject
#             subject = subject
#             recipients = {"listIds": [2]}
#             scheduled_at = (datetime.now(pytz.utc) + timedelta(minutes=1)).isoformat()
#             email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(scheduled_at =scheduled_at ,sender=sender, name=name,  subject=subject,  recipients=recipients,html_content=content) # CreateEmailCampaign | Values to create a campaign
#             api_response = api_instance.create_email_campaign(email_campaigns)
#             pprint(api_response)
#             return redirect('newsletter')


def sendEmail(sujet, contenu):

    try:
        subject = sujet
        content= contenu
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] =  settings.SMTP_API_KEY
        api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
        sender = {"name": 'La pierre de lune', "email": 'medjaoui.imene@gmail.com'}
        name = subject
        subject = subject
        recipients = {"listIds": [2]}
        scheduled_at = (datetime.now(pytz.utc) + timedelta(minutes=1)).isoformat()
        unsubscribe_id = '65fd9b792c61483dba7e8b8e'
        email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(scheduled_at =scheduled_at ,sender=sender, name=name,  subject=subject,  recipients=recipients,html_content=content, unsubscription_page_id=unsubscribe_id, inline_image_activation=True) # CreateEmailCampaign | Values to create a campaign

        api_response = api_instance.create_email_campaign(email_campaigns)
        pprint(api_response)
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
        cart = cart_item.cart

        # Calculate the total price of the cart
        total_price = cart.cartitem_set.aggregate(total=Sum('item_price'))['total']

        # Return the item price and total price as JSON response
        return JsonResponse({'item_price': item_price, 'total_price': total_price})
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

        # Get the associated Article instance
        article = cart_item.article

        # Increment the article's stock by the CartItem's quantity
        article.stock += cart_item.quantity
        article.save()

        item_price = cart_item.item_price
        # Delete the Item
        cart_item.delete()

        return JsonResponse({'success': True, 'message': 'Item successfully deleted', 'item_price': item_price})
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



def submit_feedback(request):
    if request.method == 'POST':
        contenu = request.POST.get('contenu')

        user_id = request.user.id if request.user.is_authenticated else None

        # Create a Feedback object and save it to the database
        feedback = Feedback(
            contenu=contenu,
            date_envoi=timezone.now(),
            utilisateur_id=user_id,
            etat=0 
        )
        feedback.save()

        messages.success(request, 'Feedback submitted successfully!')
        return redirect('panier')  # Redirect to a success page or another URL
    else:
        # Handle non-POST requests as needed
        return render(request, 'accueil.html')
