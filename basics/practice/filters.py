import django_filters
from django_filters import filters
from .models import *
from django.db.models import Q

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'   

class PoductFilter(django_filters.FilterSet):
    # name = filters.CharFilter(method='filter_by_all_name_fields', label='search')
    class Meta:
        model = Product
        fields = ('category',)
        # def filter_by_all_name_fields(self, queryset,  value):
        #     return queryset.filter(
        #     Q(name__icontains=value) | Q(company__icontains=value))
    



    