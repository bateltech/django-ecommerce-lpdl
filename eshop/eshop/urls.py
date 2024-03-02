from django.contrib import admin
from django.urls import path, include
import ecommerce.views as views


urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('admin/', admin.site.urls),
    path('', include('ecommerce.urls')),
    #path('admin/', include('admin_black.urls')),
    path('update_quantity_ajax/<int:item_id>/<int:new_quantity>/', views.update_quantity_ajax, name='update_quantity_ajax'), 
    path ('delete_Cart_item_ajax/<int:item_id>/', views.delete_Cart_item_ajax, name = 'delete_Cart_item_ajax'),
    path('get_item_price/<int:item_id>/', views.get_item_price, name='get_item_price'),


    path ('delete_Voyance_ajax/<int:item_id>/', views.delete_Voyance_ajax, name = 'delete_Voyance_ajax'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)