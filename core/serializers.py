from rest_framework import serializers
from .models import Country, Category
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_flag', 'country_currency']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'country', 'category_title', 'price_per_kilo']


