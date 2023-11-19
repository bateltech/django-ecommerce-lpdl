# views.py
from django.http import HttpResponse
from rest_framework import viewsets
from .models import TailleArticle, Commande, Pierre, Categorie, SousCategorie, Commentaire, TagBesoin, DetailCommande, PrixArticle, Article, Feedback, ClientUser, Wishlist
from .serializers import CommandeSerializer, PierreSerializer, CategorieSerializer, SousCategorieSerializer, CommentaireSerializer, TagBesoinSerializer, DetailCommandeSerializer, PrixArticleSerializer, ArticleSerializer, FeedbackSerializer, UserSerializer, WishlistSerializer
from django.views.decorators.csrf import csrf_protect
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Vues des fonctionnalités
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout  # Importez les fonctions authenticate et login
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

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


def accueil_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    return render(request, 'accueil.html', {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur})

def articles_view(request):
    return render(request, 'articles.html')

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
    return render(request, 'conditions.html',context)

def pierres_view(request):
    pierres = Pierre.objects.all()
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'pierres': pierres, 'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'pierres.html', context)
 
def erreur_view(request, exception=None):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
    return render(request, 'erreur.html', context)

def resetpwrd_view(request):
    return render(request, 'resetpwrd.html')

def panier_view(request):
    return render(request, 'panier.html')

def checkout_view(request):
    return render(request, 'checkout.html')

@login_required()  # A CHERCHER COMMENT L'UTILISER
def profil_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'user': utilisateur}
    return render(request, 'profil.html', context)

@csrf_protect
def signup_view(response):
    if response.method == "POST":
        form = SignupForm(response.POST)
        if form.is_valid():
                print("HURRAAAAY SUCCESS")
                user = form.save()
                login(response, user)  # Log in the user after registration
                return redirect('accueil')  


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


from django.contrib import messages

def update_personal_info(request):
    if request.method == 'POST':
        user = request.user
        user.last_name = request.POST.get('nom')
        user.first_name = request.POST.get('prenom')
        user.birthdate = request.POST.get('dob')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone')
        user.save()
        messages.success(request, 'Informations personnelles mises à jour avec succès.')
        request.session['update_success'] = True  # Stockez un indicateur de succès dans la session

    return redirect('profil')

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            
            request.session['password_success'] = True  # Stockez un indicateur de succès dans la session
            return redirect('profil')  # Replace 'profile' with your profile page URL name
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('profil')


