# views.py
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import TailleArticle, Commande, Pierre, Categorie, SousCategorie, Commentaire, TagBesoin, DetailCommande, PrixArticle, Article, Feedback, ClientUser
from .serializers import CommandeSerializer, PierreSerializer, CategorieSerializer, SousCategorieSerializer, CommentaireSerializer, TagBesoinSerializer, DetailCommandeSerializer, PrixArticleSerializer, ArticleSerializer, FeedbackSerializer, UserSerializer
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

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


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


# Vues des fonctionnalités
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login  # Importez les fonctions authenticate et login
# from .models import ClientUser  # Importez le modèle ClientUser personnalisé depuis votre propre application


def accueil_view(request):
    return render(request, 'accueil.html')

def articles_view(request):
    return render(request, 'articles.html')

def mentions_view(request):
    return render(request, 'mentions.html')

# def inscription_view(request):
#     return render(request, 'inscription.html')

def connexion_view(request):
    return render(request, 'connexion.html')

def conditions_view(request):
    return render(request, 'conditions.html')

def pierres_view(request):
    return render(request, 'pierres.html')
 
def erreur_view(request):
    return render(request, 'erreur.html')

def resetpwrd_view(request):
    return render(request, 'resetpwrd.html')

def panier_view(request):
    return render(request, 'panier.html')

def checkout_view(request):
    return render(request, 'checkout.html')

# @login_required()  A CHERCHER COMMENT L'UTILISER
def profil_view(request):
    return render(request, 'profil.html')

# @csrf_protect
# def signup_view(request):
#     print("this is signup")
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if password == confirm_password:

#             if form.is_valid():
#                 user = form.save()
#                 # Hasher le mot de passe
#                 hashed_password = make_password(password)
#                 # Utilisez la méthode create_user pour créer un nouvel utilisateur
#                 user = ClientUser.objects.create_user(
#                     username=email,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     password=hashed_password,
#                     #role=101  # Le rôle à 101 = client simple
#                 )
#                 user.save()
#                 print("this is the first name ",first_name)
#                 print("this is the last name ",last_name)
#                 print("this is the email ",email)
#                 print("this is the password ",confirm_password)

#             # Connectez automatiquement l'utilisateur après l'inscription
#                 user = authenticate(request, username=email, password=password)
#                 if user is not None:
#                     login(request, user)

#             # Redirigez vers la page de connexion
#             return redirect('connexion')  # Assurez-vous que 'connexion.html' est l'URL de votre page de connexion
        
#         else:
#             print("mdp non identiques")
#             # Gérer le cas où les mots de passe ne correspondent pas
#             return render(request, 'inscription.html', {'error_message': 'Les mots de passe ne correspondent pas'})
#     else:
#         form = SignupForm()
#         return render(request, 'inscription.html', {'form': form})


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