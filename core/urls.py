from django.urls import path
from . import views, api_views
from django.shortcuts import redirect
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Auth
    path('', lambda request: redirect('login')),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path("get-cities/", views.get_cities, name="get_cities"),
    path("get-districts/", views.get_districts, name="get_districts"),
    path("get-subdistricts/", views.get_subdistricts, name="get_subdistricts"),
    path("check-ongkir/", views.check_ongkir, name="check_ongkir"),
    path('calculate/', views.calculate_price, name='calculate_price'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Country CRUD
    path('countries/', views.country_list, name='country_list'),
    path('countries/create/', views.country_create, name='country_create'),
    path('countries/<int:pk>/update/', views.country_update, name='country_update'),
    path('countries/<int:pk>/delete/', views.country_delete, name='country_delete'),

    # Category CRUD
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # API
    path('api/login/', obtain_auth_token, name='api-login'),
    path('api/countries/', api_views.api_countries, name='api_countries'),
    path('api/categories/', api_views.api_categories, name='api_categories'),
    path('api/destination/', api_views.api_destination, name='api_destination'),
    path('api/calculate/', api_views.api_calculate, name='api_calculate'),
]
