from django.contrib import admin
from django.urls import path, include
import ecommerce.views as views

urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('admin/', admin.site.urls),
    path('lapierredelune/', include('ecommerce.urls')),

]