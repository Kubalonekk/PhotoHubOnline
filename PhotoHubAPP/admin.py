from django.contrib import admin
from .models import UserProfile, Post, Obserwowani, Komentarz, ObserwowaniPowiadomienia, Historia


class HistoriaAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'czas',
        'aktywny',
    ]

    search_fields = [
        'aktywny__user',
        
    ]

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Obserwowani)
admin.site.register(Komentarz)
admin.site.register(ObserwowaniPowiadomienia)
admin.site.register(Historia, HistoriaAdmin)




