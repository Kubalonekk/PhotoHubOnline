"""photohub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('login/',
         LoginView.as_view(template_name='PhotoHubAPP/login.html'),
         name='login'),
    path('account/', views.account, name='account'),
    path('home/', views.home, name='home'),
    path('followers/', views.followers, name='followers'),
    path('followers/yours/', views.yours_followers, name='yours_followers'),
    path('add_follow/<int:pk>/', views.add_follow, name='add_follow'),
    path('profil_detail/<int:pk>/', views.profil_detail, name='profil_detail'),
    path('un_follow/<int:pk>/', views.un_follow, name='un_follow'),
    path('your_profile/', views.your_profile, name='your_profile'),
    path('followers/list/', views.followers_list, name='followers_list'),
    path('add_like/<int:pk>/', views.add_like, name='add_like'),
    # path('dodanie_komentarza/<int:pk>/', views.dodanie_komentarza, name='dodanie_komentarza'),
    path('pojedynczy_post/<int:pk>/', views.pojedynczy_post, name='pojedynczy_post'),
    path('dziennik_zdarzen/posty/', views.dziennik_zdarzen_posty, name='dziennik_zdarzen_posty'),
    path('nowy_post/', views.nowy_post, name='nowy_post'),
    path('powiadomienia/', views.powiadomienia, name='powiadomienia'),
    path('unfollow_prosba/<int:pk>/', views.unfollow_prosba, name='unfollow_prosba'),
    path('zgoda/<int:pk>/', views.zgoda, name="zgoda"),
    path('usun_powiadomienie/<int:pk>/', views.usun_powiadomienie, name='usun_powiadomienie'),
    path('odrzucenie_prosby/<int:pk>/', views.odrzucenie_prosby, name='odrzucenie_prosby'),
    path('dziennik_zdarzen/', views.dziennik_zdarzen, name='dziennik_zdarzen'),
    path('usuniete_zdarzenie/', views.usuniete_zdarzenie, name='usuniete_zdarzenie'),
    path('usun_post/<int:pk>/', views.usun_post, name="usun_post"),
    path('usun_komentarz/<int:pk>/', views.usun_komentarz, name="usun_komentarz"),
    path('ukryj_post/<int:pk>/', views.ukryj_post, name="ukryj_post"),
    path('ukryte_posty/', views.ukryte_posty, name="ukryte_posty"),
    path('odkryj_post/<int:pk>/', views.odkryj_post, name="odkryj_post"),


]


if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 