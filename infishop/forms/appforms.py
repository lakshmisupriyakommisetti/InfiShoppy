from infishop.models import Category, Product, ShippingAddress
from django.forms import ModelForm
from django import forms
class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['id','category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
        }


class AddShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ['id','user']
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phoneno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone no'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal code'})
        }