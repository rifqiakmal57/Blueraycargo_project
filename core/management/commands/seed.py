from django.core.management.base import BaseCommand
from core.models import Country, Category

class Command(BaseCommand):
    help = 'Seed database with initial Country and Category data'

    def handle(self, *args, **kwargs):
        countries = [
            {"name": "Indonesia", "code": "ID"},
            {"name": "United States", "code": "US"},
            {"name": "Japan", "code": "JP"},
        ]

        categories = [
            {"name": "Electronics", "description": "Electronic goods and devices"},
            {"name": "Furniture", "description": "Home and office furniture"},
            {"name": "Clothing", "description": "Apparel and accessories"},
        ]

        for c in countries:
            Country.objects.get_or_create(**c)
        for cat in categories:
            Category.objects.get_or_create(**cat)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
