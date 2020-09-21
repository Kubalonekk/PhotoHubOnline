import django_filters
from .models import * 
from django_filters import CharFilter 


class ProfileFilter(django_filters.FilterSet):
    imie = CharFilter(field_name="imie", lookup_expr='icontains')
    nazwisko = CharFilter(field_name="nazwisko", lookup_expr='icontains')
    class Meta:
        model = UserProfile
        fields = ['imie','nazwisko']
        