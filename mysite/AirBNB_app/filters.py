import django_filters
from django_filters import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'city': ['exact'],
            'property_type': ['exact'],
            'max_guests': ['gt'],
            'price': ['gt', 'lt'],
            'rules': ['exact'],
        }
