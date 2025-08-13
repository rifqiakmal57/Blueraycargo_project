from django.shortcuts import render, redirect, get_object_or_404
from .models import Country, Category
from .forms import CountryForm, CategoryForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

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

# --- Dashboard ---
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

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
            return redirect('country_list')
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
            return redirect('country_list')
    else:
        form = CountryForm(instance=country)
    return render(request, 'core/country_form.html', {'form': form})

@login_required
def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    return redirect('country_list')

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
            return redirect('category_list')
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
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'core/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')


@login_required(login_url='login')  # nama URL login dari urls.py
def dashboard_view(request):
    return render(request, 'core/dashboard.html')
