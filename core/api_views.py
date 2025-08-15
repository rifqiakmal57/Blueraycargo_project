from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Country, Category
from django.db.models import Q

# a. Api to search Origin Country
@api_view(['GET'])
def api_countries(request):
    search = request.GET.get('search', '')
    countries = Country.objects.filter(
        Q(country_name__icontains=search) |
        Q(country_currency__icontains=search)
    ).values('id', 'country_name', 'country_flag', 'country_currency')
    return Response(list(countries))

# b. Api to search Category based on the previously selected country
@api_view(['GET'])
def api_categories(request):
    country_id = request.GET.get('country_id')
    search = request.GET.get('search', '')
    if not country_id:
        return Response({'error': 'country_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    categories = Category.objects.filter(
        country_id=country_id,
        category_title__icontains=search
    ).values('id', 'category_title', 'price_per_kilo')
    return Response(list(categories))

# c. Api to search Destination City
@api_view(['GET'])
def api_destination(request):
    search = request.GET.get('search', '')
    # Misalnya data destinasi cuma contoh hardcode
    destinations = [
        {"city": "Jakarta", "code": "JKT"},
        {"city": "Surabaya", "code": "SUB"},
        {"city": "Singapore", "code": "SGP"},
    ]
    filtered = [d for d in destinations if search.lower() in d['city'].lower()]
    return Response(filtered)

# d. Api to calculate Freight
@api_view(['POST'])
def api_calculate(request):
    """
    Body JSON:
    {
        "category_id": 1,
        "weight": 10
    }
    """
    category_id = request.data.get('category_id')
    weight = request.data.get('weight')

    if not category_id or not weight:
        return Response({'error': 'category_id and weight are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    total_price = category.price_per_kilo * float(weight)
    return Response({
        'category': category.category_title,
        'weight': weight,
        'price_per_kilo': category.price_per_kilo,
        'total_price': total_price
    })
