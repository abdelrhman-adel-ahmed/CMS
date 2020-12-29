import django_filters
from django_filters import DateFilter,CharFilter
from .models import Order,Customer

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created",lookup_expr='gte')
    end_date=DateFilter(field_name="date_created",lookup_expr='lte')
    notes=CharFilter(field_name="note",lookup_expr='icontains')
    
    class Meta:
        model=Order
        fields='__all__'
        exclude=['customer','date_created','note']

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model=Customer
        fields=['name']