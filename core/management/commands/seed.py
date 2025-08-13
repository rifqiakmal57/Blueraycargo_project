from django.core.management.base import BaseCommand
from core.models import Country, Category

class Command(BaseCommand):
    help = "Seed initial Countries and Categories"

    def handle(self, *args, **kwargs):
        # countries 
        countries_def = [
            {"country_name": "China",     "country_flag": "https://flagcdn.com/w320/cn.png", "country_currency": "CHY"},
            {"country_name": "Thailand",  "country_flag": "https://flagcdn.com/w320/th.png", "country_currency": "THB"},
            {"country_name": "Singapore", "country_flag": "https://flagcdn.com/w320/sg.png", "country_currency": "SGD"},
            {"country_name": "Indonesia", "country_flag": "https://flagcdn.com/w320/id.png", "country_currency": "IDR"},
            {"country_name": "Malaysia",  "country_flag": "https://flagcdn.com/w320/my.png", "country_currency": "MYR"},
        ]

        countries = {}
        for c in countries_def:
            obj, _ = Country.objects.get_or_create(**c)
            countries[obj.country_name] = obj

        # categories (≥10)
        cat_def = [
            # China
            {"country": countries["China"], "category_title": "Electronic",            "price_per_kilo": 250000},
            {"country": countries["China"], "category_title": "Chip",                  "price_per_kilo": 300000},
            {"country": countries["China"], "category_title": "Laptop and Computer",   "price_per_kilo": 220000},
            {"country": countries["China"], "category_title": "Home Appliance",        "price_per_kilo": 180000},
            # Thailand
            {"country": countries["Thailand"], "category_title": "Garments",   "price_per_kilo": 200000},
            {"country": countries["Thailand"], "category_title": "Food",       "price_per_kilo": 160000},
            # Singapore
            {"country": countries["Singapore"], "category_title": "Spare parts", "price_per_kilo": 210000},
            {"country": countries["Singapore"], "category_title": "Medical",     "price_per_kilo": 270000},
            # Indonesia
            {"country": countries["Indonesia"], "category_title": "Furniture",   "price_per_kilo": 150000},
            {"country": countries["Indonesia"], "category_title": "Automotive",  "price_per_kilo": 190000},
            # Malaysia
            {"country": countries["Malaysia"], "category_title": "Cosmetics",    "price_per_kilo": 175000},
        ]

        for cd in cat_def:
            Category.objects.get_or_create(**cd)

        self.stdout.write(self.style.SUCCESS("Seed data inserted."))
