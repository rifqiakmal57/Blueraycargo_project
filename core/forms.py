from django import forms
from .models import Country, Category
from django.contrib.auth.models import User

# Form Country
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_name', 'country_flag', 'country_currency']

# Form Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['country', 'category_title', 'price_per_kilo']

# Form Register
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if password != password2:
            raise forms.ValidationError("Passwords do not match")

        # Cek apakah ada user dengan email + first + last sama
        if User.objects.filter(email=email, first_name=first_name, last_name=last_name).exists():
            raise forms.ValidationError("Email sudah ada, silakan login.")

        return cleaned_data
