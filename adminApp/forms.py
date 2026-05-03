from django import forms
from usersApp.models import Product 


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'discount_price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 p-3 text-sm focus:border-black outline-none transition'}),
            'category': forms.Select(attrs={'class': 'w-full border border-gray-300 p-3 text-sm focus:border-black outline-none transition bg-white'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 p-3 text-sm focus:border-black outline-none transition'}),
            'discount_price': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 p-3 text-sm focus:border-black outline-none transition'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 p-3 text-sm focus:border-black outline-none transition', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-3 text-sm focus:border-black outline-none transition'}),
        }