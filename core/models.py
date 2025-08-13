from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    country_flag = models.URLField()
    country_currency = models.CharField(max_length=50, default="IDR")

    def __str__(self):
        return self.country_name


class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="categories")
    category_title = models.CharField(max_length=100, default="Umum")  # default biar migrasi aman
    price_per_kilo = models.PositiveIntegerField(default=0)  # default biar migrasi aman

    class Meta:
        unique_together = ("country", "category_title")

    def __str__(self):
        return f"{self.category_title} - {self.country.country_name}"
