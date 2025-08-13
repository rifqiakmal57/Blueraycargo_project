from django.contrib import admin
from .models import Country, Category

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "country_name", "country_currency")
    search_fields = ("country_name", "country_currency")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_title", "country", "price_per_kilo")
    list_filter = ("country",)
    search_fields = ("category_title",)
