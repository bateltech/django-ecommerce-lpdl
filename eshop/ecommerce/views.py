# views.py
from django.http import HttpResponse
from rest_framework import viewsets
from .models import TailleArticle, Commande, Pierre, Categorie, SousCategorie, Commentaire, TagBesoin, DetailCommande, PrixArticle, Article, Feedback, ClientUser, Wishlist
from .serializers import CommandeSerializer, PierreSerializer, CategorieSerializer, SousCategorieSerializer, CommentaireSerializer, TagBesoinSerializer, DetailCommandeSerializer, PrixArticleSerializer, ArticleSerializer, FeedbackSerializer, UserSerializer, WishlistSerializer
from django.views.decorators.csrf import csrf_protect
from .forms import SignupForm, LoginForm, PersonalInfoForm, PasswordResetForm
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
from django.contrib import messages

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



# def pierres_view(request):
#     pierres = Pierre.objects.all()
#     utilisateur_connecte = request.user.is_authenticated
#     prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
#     context = {'pierres': pierres, 'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur}
#     return render(request, 'pierres.html', context)
 


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
    
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'user': utilisateur}
    return render(request, 'favoris.html', context)


@login_required()  # A CHERCHER COMMENT L'UTILISER
def commentaires_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'user': utilisateur}
    return render(request, 'commentaires.html', context)


@login_required()  # A CHERCHER COMMENT L'UTILISER
def historique_view(request):
    utilisateur_connecte = request.user.is_authenticated
    prenom_utilisateur = request.user.first_name if utilisateur_connecte else None
    utilisateur = request.user if utilisateur_connecte else None
    
    context = {'utilisateur_connecte': utilisateur_connecte, 'prenom_utilisateur': prenom_utilisateur, 'user': utilisateur}
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

