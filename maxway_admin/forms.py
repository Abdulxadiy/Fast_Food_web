from django import forms
from maxway_users import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={'class': 'form-control'}),
            "image": forms.FileInput(attrs={
                'class': 'form-control',
                'onchange': 'loadfile(event)'}
            ),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "category": forms.Select(attrs={'class': 'form-control'})
        }


class UsersForm(forms.ModelForm):
    class Meta:
        model = models.Users
        fields = '__all__'
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.Textarea(attrs={'class': 'form-control'})
        }