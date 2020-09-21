from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count, Avg
from .models import UserProfile, Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, KomentarzForm, NowyPostForm
from .filters import ProfileFilter
from django.contrib.sessions.models import Session
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponseRedirect


# Create your views here.
def update(request):
    if request.user.userprofile.ukryty == False:
            try:
                session_id = request.session['licznik']
                counter = ObserwowaniPowiadomienia.objects.filter(obserwowany=request.user.userprofile).count()
                request.session['licznik'] = counter
            except:
                counter = ObserwowaniPowiadomienia.objects.filter(obserwowany=request.user.userprofile).count()
                request.session['licznik'] = counter
    else:
        try:
            session_id = request.session['licznik']
            counter = Obserwowani.objects.filter(obserwowany=request.user.userprofile, prosba=True, zgoda=False ).count()
            request.session['licznik'] = counter
        except:
            counter = Obserwowani.objects.filter(obserwowany=request.user.userprofile, prosba=True, zgoda=False ).count()
            request.session['licznik'] = counter

def index(request):
    if request.user.is_authenticated: 
        func = update(request)
        followers = Obserwowani.objects.filter(obserwujacy=request.user.userprofile, prosba=True, zgoda=True)
        posty = Post.objects.all()
        cos = Post.objects.filter(likes=request.user.userprofile.id)
        formm = KomentarzForm()

        if request.method == "POST":
            form = NowyPostForm(request.POST, request.FILES)
            if form.is_valid():
                formularz = form.save(commit=False)
                tytul = form.cleaned_data.get('tytul')
                formularz.userprofile = request.user.userprofile
                formularz.save()
                post_id = formularz

                nowe_zdarzenie = Historia.objects.create(
                    aktywny = request.user.userprofile,
                    post = 2,
                    czas = datetime.now(),
                    tytul = tytul,
                    post_id = post_id,
                )
                return redirect('index')
            else:
                messages.info(request, 'Cos poszlo nie tak')
        else:
            form = NowyPostForm()


        context = {
            'posty':posty,
            'followers':followers,
            'form': form,
            'formm': formm,
        }
    else:
        messages.success(request, 'Aby mieć dostęp do tej strony, załóż konto')
        return redirect('home')

    
    return render(request, 'PhotoHubAPP/index.html', context)

def register(request):
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)

    if form.is_valid():
        new_user = form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        imie = form.cleaned_data.get('imie')
        nazwisko = form.cleaned_data.get('nazwisko')
        profile = UserProfile.objects.create(
            user=new_user,
            imie=imie,
            nazwisko=nazwisko,
            email=email
        )
        messages.success(request, 'Konto zalozone pomyslnie')
        authenticated_user = authenticate(  # automatyczne zalogowanie po utworzeniu konta
            username=new_user.username,
            password=request.POST['password1'])
        login(request, authenticated_user)
        follow = Obserwowani.objects.create(
            obserwowany=profile, 
            obserwujacy=profile, 
            imie=profile.imie, 
            nazwisko=profile.nazwisko,
            prosba=True,
            zgoda=True,)
        return HttpResponseRedirect(reverse('index'))

    context = {'form': form}
    return render(request, 'PhotoHubAPP/register.html', context)



def logout_view(request):
    logout(request)
    return redirect('index')

def account(request):
    if request.user.is_authenticated:
        form = UserProfileForm(instance=request.user.userprofile)
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ustawienia zostały zmienione pomyślnie')
                return redirect('your_profile')
    else:
        messages.success(request, 'Aby mieć dostęp do konta, najpierw musisz je założyć')
        return redirect('home')

    context = {
        'form':form,
    }
  
    return render(request, 'PhotoHubAPP/account.html', context)

def home(request):

    return render(request, 'PhotoHubAPP/home.html')

def followers(request):
    

    if request.user.is_authenticated:
        func = update(request)
        profiles = UserProfile.objects.all().order_by('-data_zalozenia')
        MyFilter = ProfileFilter(request.GET, queryset=profiles)
        profiles = MyFilter.qs

     


    else:
        messages.info(request, 'Aby mieć dostęp do obserwujących, najpierw musisz założyć konto')
        return redirect('home')

    context = {
        'profiles':profiles,
        'MyFilter': MyFilter,
    }

    return render(request, 'PhotoHubAPP/followers.html', context)

def yours_followers(request):

    if request.user.is_authenticated:
        profiles = Obserwowani.objects.filter(obserwujacy=request.user.userprofile, prosba=True, zgoda=True).order_by('-data_stworzenia')
        MyFilter = ProfileFilter(request.GET, queryset=profiles)
        profiles = MyFilter.qs

    else:
        messages.info(request, 'Aby mieć dostęp do obserwujących, najpierw musisz założyć konto')
        return redirect('home') 

    context = {
        'profiles':profiles,
        'MyFilter': MyFilter,
    }

    return render(request, 'PhotoHubAPP/yours_followers.html', context)



def add_follow(request, pk):

    profile = UserProfile.objects.get(pk=pk)
    if profile.ukryty == True:
        new_follow = Obserwowani.objects.create(
            obserwujacy= request.user.userprofile,
            obserwowany= profile,
            imie=profile.imie,
            nazwisko=profile.nazwisko,
            prosba=True
        )
        messages.info(request, 'Wyslales prośbę o obserwowanie '+ profile.imie + ' ' + profile.nazwisko) 
        return redirect('profil_detail', pk)
    else:
        new_follow = Obserwowani.objects.create(
            obserwujacy= request.user.userprofile,
            obserwowany= profile,
            imie=profile.imie,
            nazwisko=profile.nazwisko,
            prosba=True,
            zgoda=True,
        )
        follow_powiadomienia = ObserwowaniPowiadomienia.objects.create(
            obserwacja = new_follow,
            obserwujacy=new_follow.obserwujacy,
            obserwowany=new_follow.obserwowany,

        )
        follow_historia = Historia.objects.create(
            aktywny= new_follow.obserwujacy,
            pasywny= new_follow.obserwowany,
            follow= 2,
            czas=datetime.now()
        )
        name = profile.imie
        last_name = profile.nazwisko
            
        messages.info(request, 'Zacząłeś obserwować użytkownika '+ name + ' ' + last_name) 
        return redirect('profil_detail', pk)

def un_follow(request, pk):
    profile = UserProfile.objects.get(pk=pk)
    del_profile = Obserwowani.objects.get(
        obserwujacy= request.user.userprofile,
        obserwowany= profile,
    )
    un_follow_historia = Historia.objects.create(
            aktywny= del_profile.obserwujacy,
            pasywny= del_profile.obserwowany,
            follow= 1,
            czas=datetime.now(),
    )
    del_profile.delete()
    name = profile.imie
    last_name = profile.nazwisko

    messages.info(request, 'Przestałeś obserwować użytkownika '+ name +' ' + last_name)
    return redirect('profil_detail', pk)

def usun_powiadomienie(request, pk):
    powiadomienia = ObserwowaniPowiadomienia.objects.get(obserwacja=pk)
    powiadomienia.delete()
    return redirect('powiadomienia')

def odrzucenie_prosby(request, pk):
    follow = Obserwowani.objects.get(
        pk=pk,        
    )
    follow.delete()
    return redirect('powiadomienia')


def unfollow_prosba(request, pk):
    profile = UserProfile.objects.get(pk=pk)
    prosba = Obserwowani.objects.get(
        obserwujacy= request.user.userprofile,
        obserwowany= profile,
        prosba=True,
    )
    prosba.delete()
    messages.info(request, 'Usunąłeś prośbe obserwacji '+ profile.imie +' ' + profile.nazwisko)
    return redirect('profil_detail', pk)



def profil_detail(request, pk):
    func = update(request)
    formm = KomentarzForm()
    profile = UserProfile.objects.get(pk=pk)
    if profile == request.user.userprofile:
        return redirect('your_profile')
    else:
        pass
    posty = Post.objects.filter(userprofile=pk)
    if profile.ukryty == True:
        try:
            followers = Obserwowani.objects.get(obserwujacy=request.user.userprofile, obserwowany=pk, prosba=True, zgoda=True)
            ukryty = False
            follow = True
            prosba = False
        except:
            if Obserwowani.objects.filter(obserwujacy=request.user.userprofile, obserwowany=pk, prosba=True, zgoda=False).exists():
                prosba = True
                ukryty = True
                follow = False
            else:
                ukryty = True
                follow = False
                prosba = False 
                pass
    else:
        try:
            # jesli bede followal ją to ukryty jest false po to aby moc wyswietlic profil.  TO NIE JEST ZMIENNA PRZY OBSERWOWANYCH!
            followers = Obserwowani.objects.get(obserwujacy=request.user.userprofile, obserwowany=pk)
            follow = True
            ukryty = False # zmienna do szablonu
            prosba = False
        except:
            follow = False
            if profile.ukryty == True:
                ukryty = True
                prosba = False
            else:
                ukryty = False
                prosba = False
        # tutaj bedzie kod ktory bedzie zaslanial posty uzytkownika
        
    

    context = {
        'ukryty': ukryty,
        'profile': profile,
        'posty': posty,
        'follow': follow,
        'prosba': prosba,
        'formm': formm,
    }

    return render(request, 'PhotoHubAPP/profil_detail.html', context)

def your_profile(request):
    posty = Post.objects.filter(userprofile=request.user.userprofile).order_by('-data_stworzenia')
    formm = KomentarzForm()

    context = {
        'posty': posty,
        'formm': formm,
    }

    return render(request, 'PhotoHubAPP/your_profile.html', context)


def followers_list(request):

    if request.user.is_authenticated:
        profiles = Obserwowani.objects.filter(obserwowany=request.user.userprofile, prosba=True, zgoda=True).order_by('-data_stworzenia')
        MyFilter = ProfileFilter(request.GET, queryset=profiles)
        profiles = MyFilter.qs
        print(profiles)

    else:
        messages.info(request, 'Aby mieć dostęp do obserwujących, najpierw musisz założyć konto')
        return redirect('home') 

    context = {
        'profiles':profiles,
        'MyFilter': MyFilter,
    }

    return render(request, 'PhotoHubAPP/followers_list.html', context)

#Dodanie lajka do postu
def add_like(request, pk):
    post = Post.objects.get(id=pk)
    if post.likes.filter(user=request.user).exists():
        historia = Historia.objects.create(
            aktywny=request.user.userprofile,
            pasywny=post.userprofile,
            like=1,
            post_id=post,
            czas=datetime.now(),
        )
        post.like_counter -= 1
        post.likes.remove(request.user.userprofile)
        post.save()
    else:
        historia = Historia.objects.create(
            aktywny=request.user.userprofile,
            pasywny=post.userprofile,
            like=2,
            post_id=post,
            czas=datetime.now(),
        )
        post.like_counter += 1
        post.likes.add(request.user.userprofile)
        post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# 

# def dodanie_komentarza(request, pk):
#     post = Post.objects.get(id=pk)
#     if request.method == 'POST':
#         form = KomentarzForm(request.POST)
#         if form.is_valid():
#             komentarz = form.save(commit=False)
#             komentarz.userprofile = request.user.userprofile
#             komentarz.post = post
#             komentarz.save()
#             post.komentarze_counter += 1
#             post.save()
#             return redirect('index') 
#         else:
#             messages.info(request, 'Cos poszlo nie tak')
#             return redirect('index') 
#     else:
#         form = KomentarzForm()
    
#     context = {
#         'form':form,
#     }

#     return render(request, 'PhotoHubAPP/dodanie_komentarza.html', context)




def pojedynczy_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = KomentarzForm(request.POST)
        if form.is_valid():
            komentarz = form.save(commit=False)
            komentarz.userprofile = request.user.userprofile
            komentarz.post = post
            historia_object = komentarz.save()
            post.komentarze_counter += 1
            historia = Historia.objects.create(
                aktywny= request.user.userprofile,
                pasywny= post.userprofile,
                post_id= post,
                komentarz=2,
                czas=datetime.now(),
            )
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, 'Cos poszlo nie tak')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = KomentarzForm()

    context = {
        "post": post,
        "formm": form,
    }
    return render(request, 'PhotoHubAPP/pojedynczy_post.html', context)



def dziennik_zdarzen_posty(request):
    func = update(request)
    zdarzenia_posty = Post.objects.filter(userprofile = request.user.userprofile).order_by("-data_stworzenia")
    print(zdarzenia_posty)

    context = {
        'zdarzenia_posty': zdarzenia_posty,
    }

    return render(request, 'PhotoHubAPP/dziennik_zdarzen_posty.html', context)



def nowy_post(request):

    if request.method == "POST":
        form = NowyPostForm(request.POST, request.FILES)
        if form.is_valid():
            formularz = form.save(commit=False)
            formularz.userprofile = request.user.userprofile
            formularz.save()
            return redirect('index')
        else:
            messages.info(request, 'Cos poszlo nie tak')
    else:
        form = NowyPostForm()



    context = {
        'form': form,

    }

    return render(request, 'PhotoHubAPP/nowy_post.html', context)


def powiadomienia(request):
    func = update(request)
    if request.user.userprofile.ukryty == True:
        followers = Obserwowani.objects.filter(obserwowany=request.user.userprofile, prosba=True, zgoda=False )
    else:
        followers = ObserwowaniPowiadomienia.objects.filter(obserwowany=request.user.userprofile)
    

    context = {
        'followers': followers,

    }
    return render(request, 'PhotoHubAPP/powiadomienia.html', context)

def zgoda(request, pk):
    followers = Obserwowani.objects.get(id=pk)
    followers.zgoda = True
    followers.save()
    follow_historia = Historia.objects.create(
            aktywny= followers.obserwujacy,
            pasywny= followers.obserwowany,
            follow= 2,
            czas=datetime.now()
        )
    return redirect('powiadomienia')


def dziennik_zdarzen(request):
    func = update(request)
    zdarzenia = Historia.objects.filter(
        Q(aktywny= request.user.userprofile) | Q(pasywny= request.user.userprofile),
    ).exclude(usuniete_zdarzenie= request.user.userprofile).order_by('-czas')

    context = {
        'zdarzenia': zdarzenia,
    }
    return render(request, 'PhotoHubAPP/dziennik_zdarzen.html', context)

def usuniete_zdarzenie(request):

    zdarzenia = Historia.objects.filter(
        Q(aktywny= request.user.userprofile) | Q(pasywny= request.user.userprofile),       
    )
    for zdarzenie in zdarzenia:
        zdarzenie.usuniete_zdarzenie.add(request.user.userprofile)

    
    return redirect('dziennik_zdarzen')

def ukryj_post(request, pk):
    post = Post.objects.get(id=pk)
    post.ukryj_post.add(request.user.userprofile)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def odkryj_post(request, pk):
    post = Post.objects.get(id=pk)
    print('siema')
    post.ukryj_post.remove(request.user.userprofile)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def ukryte_posty(request):
    posty = Post.objects.filter(
        ukryj_post= request.user.userprofile
    )
    print(posty)
    context = {
        'posty': posty,

    }

    return render(request, 'PhotoHubAPP/ukryte_posty.html', context)


def usun_komentarz(request, pk):
    komentarz_do_usuniecia = Komentarz.objects.get(id=pk)
    historia = Historia.objects.create(
        aktywny= request.user.userprofile,
        pasywny= komentarz_do_usuniecia.userprofile,
        post_id= komentarz_do_usuniecia.post,
        komentarz=1,
        czas=datetime.now(),
    )
    komentarz_do_usuniecia.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def usun_post(request, pk):
    post_do_usuniecia = Post.objects.get(id=pk)
    nowe_zdarzenie = Historia.objects.create(
        aktywny = request.user.userprofile,
        tytul = post_do_usuniecia.tytul,
        post = 1,
        czas = datetime.now(),
    )
    post_do_usuniecia.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

