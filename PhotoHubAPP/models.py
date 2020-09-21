
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    STATUS = (
        ('', 'Twój status'),
        ('W zwiazku','W zwiazku'),
        ('Wolny/a','Wolny/a'),
        ('To skomplikowane','To skomplikowane'),
    )

    PLEC = (
        ('','Podaj swoja plec'),
        ('Mezczyzna','Męzczyzna'),
        ('Kobieta','Kobieta'),

    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imie = models.CharField(max_length=200, null=True)
    nazwisko = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, blank=True)
    zdjecie_profilowe = models.ImageField(default='user.png',null=True)
    data_zalozenia = models.DateTimeField(auto_now_add=True, null=True)
    opis = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, null=True, blank=True)
    wyksztalcenie =  models.CharField(max_length=150, null=True, blank=True)
    plec = models.CharField(max_length=50, choices=PLEC, null=True, blank=True)
    ukryty = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.imie} {self.nazwisko}"
    

class Post(models.Model):
     userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='posts')
     tytul = models.CharField(max_length=150, null=True)
     tekst = models.TextField(null=True)
     obrazek = models.ImageField(null=True, blank=True)
     data_stworzenia = models.DateTimeField(auto_now_add=True, null=True)
     like_counter = models.DecimalField(decimal_places=0, max_digits=10, default=0, null=True)
     likes = models.ManyToManyField(UserProfile, null=True, blank=True)
     komentarze_counter = models.DecimalField(decimal_places=0, max_digits=10, default=0, null=True)
     ukryj_post = models.ManyToManyField(UserProfile, blank=True, related_name='ukryj_post_set', help_text="Użytkownicy ktorzy beda na tej liscie nie beda widzieli tego posta") 
     

     def __str__(self):
         return self.tytul

class Obserwowani(models.Model):
    obserwujacy = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    obserwowany = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name = 'obserwowany_set')
    data_stworzenia = models.DateTimeField(auto_now_add=True, null=True)
    imie = models.CharField(max_length=200, null=True, help_text="Imię osoby która jest obserwowana")
    nazwisko = models.CharField(max_length=200, null=True, help_text="Nazwisko osoby która jest obserwowana")
    prosba = models.BooleanField(default=False, help_text="Dotyczy tylko obserwowania profili ukrytych")
    zgoda = models.BooleanField(default=False, help_text="Dotyczy tylko obserwowania profili ukrytych")


    def __str__(self):
        if self.prosba == True and self.zgoda == False:
            return f"{self.obserwujacy} prośba  {self.obserwowany}"
        elif self.prosba == True and self.zgoda == True:
            return f"{self.obserwujacy} obserwuje  {self.obserwowany}"
        else:    
            return f"{self.obserwujacy} obserwuje  {self.obserwowany}"
     

class Komentarz(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_set")
    data_dodania = models.DateTimeField(auto_now_add=True)
    tresc = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.userprofile} skomentował  {self.post.tytul}"

class ObserwowaniPowiadomienia(models.Model):
    obserwacja = models.ForeignKey(Obserwowani, on_delete=models.CASCADE)
    obserwujacy = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    obserwowany = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name = 'obserwowany_sett')



class Historia(models.Model):
    aktywny = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name = 'aktywny')
    pasywny = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name = 'pasywny')
    komentarz_id = models.ForeignKey(Komentarz, on_delete=models.CASCADE, null=True, blank=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    follow_id = models.ForeignKey(Obserwowani, on_delete=models.CASCADE, null=True, blank=True)
    like = models.IntegerField(default=0, help_text="0 - brak działania, 1 - usunięcie, 2 dodanie, 5 - wyświetlone")
    komentarz = models.IntegerField(default=0, help_text="0 - brak działania, 1 - usunięcie, 2 dodanie, 5 - wyświetlone")
    post  = models.IntegerField(default=0, help_text="0 - brak działania, 1 - usunięcie, 2 dodanie, 5 - wyświetlone")
    follow = models.IntegerField(default=0, help_text="0 - brak działania, 1 - usunięcie, 2 dodanie, 5 - wyświetlone")
    czas = models.DateTimeField(blank=True, null=True)
    usuniete_zdarzenie = models.ManyToManyField(UserProfile, null=True, blank=True,help_text="Jesli na tej liscie znajduje sie uzytkownik to znaczy ze wyswietlil dane zdarzenie")
    tytul = models.CharField(null=True, blank=True, max_length=100,)
    def __str__(self):
        if self.like == 1:
            return f"{self.aktywny} usunął lajka z posta {self.post_id} użytkownika: {self.pasywny}"
        elif self.like == 2:
            return f"{self.aktywny} dodał lajka do posta {self.post_id} użytkownika: {self.pasywny}"
        elif self.follow == 1:
            return f"{self.aktywny} przestał obserwować użytkownika {self.pasywny}"
        elif self.follow == 2:
            return f"{self.aktywny} zaczął obserwować użytkownika {self.pasywny}"
        elif self.post == 1:
            return f"{self.aktywny} Usunął post {self.tytul}"
        elif self.post == 2:
            return f"{self.aktywny} Dodał post { self.tytul }"
        elif self.komentarz == 1:
            return f"{self.aktywny} Usunał komentarz z pod posta { self.post_id.tytul }"
        elif self.komentarz == 2:
            return f"{self.aktywny} Dodał komentarz do posta { self.post_id.tytul }"
    

  



