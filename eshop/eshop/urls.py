from django.contrib import admin
from django.urls import path, include
import ecommerce.views as views

urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('admin/', admin.site.urls),
    path('', include('ecommerce.urls')),
    #path('admin/', include('admin_black.urls')),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)