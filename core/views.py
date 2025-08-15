from django.shortcuts import render, redirect, get_object_or_404
from .models import Country, Category
from .forms import CountryForm, CategoryForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt


BASE = getattr(settings, "RAJAONGKIR_BASE_URL", "https://rajaongkir.komerce.id/api/v1")

def _headers():
    return {
        "key": settings.RAJAONGKIR_API_KEY,
        "Accept": "application/json",
    }

def index(request):
    provinces = []
    try:
        res = requests.get(f"{BASE}/destination/province", headers=_headers(), timeout=10)
        res.raise_for_status()
        payload = res.json()
        provinces = payload.get("data", [])
    except Exception as e:
        print("RajaOngkir get provinces error:", e, getattr(res, "text", None))
    return render(request, "ongkir/index.html", {"provinces": provinces})


def get_cities(request):
    province_id = request.GET.get("province_id")
    if not province_id:
        return JsonResponse([], safe=False)
    try:
        res = requests.get(f"{BASE}/destination/city/{province_id}", headers=_headers(), timeout=10)
        res.raise_for_status()
        return JsonResponse(res.json().get("data", []), safe=False)
    except Exception as e:
        print("get_cities error:", e, getattr(res, "text", None))
        return JsonResponse([], safe=False)


def get_districts(request):
    city_id = request.GET.get("city_id")
    if not city_id:
        return JsonResponse([], safe=False)
    try:
        res = requests.get(f"{BASE}/destination/district/{city_id}", headers=_headers(), timeout=10)
        res.raise_for_status()
        return JsonResponse(res.json().get("data", []), safe=False)
    except Exception as e:
        print("get_districts error:", e, getattr(res, "text", None))
        return JsonResponse([], safe=False)


def get_subdistricts(request):
    district_id = request.GET.get("district_id")
    if not district_id:
        return JsonResponse([], safe=False)
    try:
        res = requests.get(f"{BASE}/destination/sub-district/{district_id}", headers=_headers(), timeout=10)
        res.raise_for_status()
        return JsonResponse(res.json().get("data", []), safe=False)
    except Exception as e:
        print("get_subdistricts error:", e, getattr(res, "text", None))
        return JsonResponse([], safe=False)


def check_ongkir(request):
    origin = request.POST.get("origin")        # district ID atau subdistrict ID
    destination = request.POST.get("destination")
    weight = request.POST.get("weight") or "0"     # gram
    courier = request.POST.get("courier") or ""

    payload = {
        "origin": origin,
        "destination": destination,
        "weight": weight,
        "courier": courier,
    }

    try:
        res = requests.post(
            f"{BASE}/calculate/domestic-cost",
            headers={**_headers(), "Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
            timeout=15
        )
        res.raise_for_status()
        data = res.json()
        return JsonResponse(data.get("data", data), safe=False)
    except Exception as e:
        print("check_ongkir error:", e, getattr(res, "text", None))
        return JsonResponse({"error": "failed to fetch cost", "detail": getattr(res, "text", None)}, status=500)

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # wajib diisi
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registrasi berhasil! Silakan login.")
            return redirect('login')
        else:
            # Ambil error dari form
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login berhasil!")
            return redirect('dashboard')
        else:
            messages.error(request, "Email atau password salah")
            return redirect('login')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# --- Country CRUD ---
@login_required
def country_list(request):
    countries = Country.objects.all()
    return render(request, 'core/country_list.html', {'countries': countries})

@login_required
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CountryForm()
    return render(request, 'core/country_form.html', {'form': form})

@login_required
def country_update(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CountryForm(instance=country)
    return render(request, 'core/country_form.html', {'form': form})

@login_required
def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        country.delete()
        messages.success(request, "Country berhasil dihapus!")
    return redirect('dashboard')

# --- Category CRUD ---
@login_required
def category_list(request):
    categories = Category.objects.select_related('country').all()
    return render(request, 'core/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'core/category_form.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'core/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category berhasil dihapus!")
    return redirect('dashboard')


@login_required
def dashboard(request):
    countries = Country.objects.all()
    categories = Category.objects.all()
    provinces = []  # ambil dari API RajaOngkir
    try:
        res = requests.get(f"{BASE}/destination/province", headers=_headers(), timeout=10)
        res.raise_for_status()
        provinces = res.json().get("data", [])
    except Exception as e:
        print("RajaOngkir get provinces error:", e)

    from .forms import CountryForm, CategoryForm
    country_form = CountryForm()
    category_form = CategoryForm()

    return render(request, 'core/dashboard.html', {
        'countries': countries,
        'categories': categories,
        'provinces': provinces,
        'country_form': country_form,
        'category_form': category_form,
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Category
import requests

@csrf_exempt
@login_required
def calculate_price(request):
    if request.method == "POST":
        country_id = request.POST.get("country")
        category_id = request.POST.get("category")
        weight = float(request.POST.get("weight") or 0)

        # Ambil category dan price_per_kilo
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.category_title
            price_per_kilo = category.price_per_kilo
        except Category.DoesNotExist:
            return JsonResponse({"error":"Category tidak ditemukan"}, status=400)

        international_price = weight * price_per_kilo

        # Domestic
        origin = request.POST.get("district_origin") or request.POST.get("city_origin")
        destination = request.POST.get("district_destination") or request.POST.get("city_destination")
        weight_dom = request.POST.get("weight_dom") or "1000"
        courier = request.POST.get("courier") or ""

        BASE = getattr(settings, "RAJAONGKIR_BASE_URL", "https://rajaongkir.komerce.id/api/v1")
        headers = {"key": settings.RAJAONGKIR_API_KEY, "Accept": "application/json"}

        domestic_price = 0
        try:
            res = requests.post(
                f"{BASE}/calculate/domestic-cost",
                headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "origin": origin,
                    "destination": destination,
                    "weight": weight_dom,
                    "courier": courier,
                },
                timeout=15
            )
            res.raise_for_status()
            data = res.json().get("data", [])
            if isinstance(data, list) and data:
                # ambil cost paling gede
                domestic_price = max(item.get("cost",0) for item in data)
        except Exception as e:
            print("check_ongkir error:", e)

        total_price = international_price + domestic_price

        return JsonResponse({
            "origin": origin,
            "destination": destination,
            "category_name": category_name,
            "international_price": int(international_price),
            "domestic_price": int(domestic_price),
            "total_price": int(total_price),
        })
    return JsonResponse({"error":"Method not allowed"}, status=405)