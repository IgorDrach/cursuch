"""
Definition of urls for DreamTourRelaxAllYear.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import path


from django.conf.urls.static import static  # Импорт функции static для настройки доступа к загруженным файлам
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings  # Импорт модуля settings


urlpatterns = [ 
    path('', views.home, name='home'),  
    path('contact/', views.contact, name='contact'),  
    path('links/', views.links, name='links'),  
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),  
    path('new-tour/', views.new_tour, name='new_tour'),  
    path('edit-tour/<int:tour_id>/', views.edit_tour, name='edit_tour'),  
    path('delete-tour/<int:tour_id>/', views.delete_tour, name='delete_tour'),  
    path('add_to_cart/<int:tour_id>/', views.add_to_cart_redirect, name='add_to_cart_redirect'),  
    path('tours/category/<int:category_id>/', views.tours_by_category, name='tours_by_category'),   
    path('tours/', views.all_tours, name='all_tours'), 
    path('tours/', views.tours, name='tours'), 
    path('korsina/', views.korsina, name='korsina'),   
    path('cart/', views.cart, name='cart'),  
    path('manager/orders/', views.manager_orders, name='manager_orders'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('remove-from-cart/<int:tour_id>/', views.remove_from_cart, name='remove_from_cart'),  
    path('booking/', views.booking, name='booking'),  
    path('success_tour/', views.success_tour, name='success_tour'),  
    path('anketa/', views.anketa, name='anketa'),  
    path('success/', views.success_view, name='success'),   
    path('registration/', views.registration, name='registration'),  
    path('blog/', views.blog, name='blog'),  
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),  
    path('newpost/', views.newpost, name='newpost'),   
    path('videopost/', views.videopost, name='videopost'),   
    path('login/',  
        LoginView.as_view( 
            template_name='app/login.html',  
            authentication_form=forms.BootstrapAuthenticationForm,  
            extra_context={  
                'title': 'Авторизация',  
                'year': datetime.now().year,  
            }  
        ),  
        name='login'  # Добавлена запятая здесь
    ), 
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  
    path('admin/', admin.site.urls),  
] 
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns += staticfiles_urlpatterns() 