#forms.py
from io import BytesIO

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from .utils import generate_image  # Assuming you have a generate_image function in utils.py
from urllib.request import urlopen
from django.core.files.base import ContentFile
from django.core.files import File
from .models import UserProfile


class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['item_name', 'quantity']


class LoginForm(AuthenticationForm):
    # Add any custom fields if necessary, otherwise just use the standard ones
    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'})
    )


class PantryItemForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = ['name', 'quantity']

    def save(self, commit=True):
        pantry_item = super().save(commit=False)
        image_data = generate_image(pantry_item.name)
        if image_data and 'image_url' in image_data:  # Replace 'image_url' with the actual key
            image_url = image_data['image_url']
            response = urlopen(image_url)
            io = BytesIO(response.read())
            pantry_item.image.save(f"{pantry_item.name}.jpg", File(io), save=False)

        if commit:
            pantry_item.save()
        return pantry_item


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipes
        fields = ['recipe_name', 'recipe_desc', 'recipe_preptime', 'recipe_cooktime',
                  'recipe_peanut', 'recipe_Dairy', 'recipe_vegetarian', 'recipe_vegan']
        labels = {'recipe_name': 'Recipe Name', 'recipe_desc': 'Cooking Instructions', 'recipe_preptime': 'Prep Time',
                  'recipe_cooktime': 'Cook Time', 'recipe_peanut': 'Contains Peanuts', 'recipe_Dairy': 'Contains Dairy',
                  'recipe_vegetarian': 'Vegetarian', 'recipe_vegan': 'Vegan'}


class RecipeIngredientForm(forms.Form):
    ingredient_name = forms.ModelChoiceField(queryset=Ingredients.objects.all())
    unit = forms.ModelChoiceField(queryset=MeasurementUnits.objects.all())
    quantity = forms.ModelChoiceField(queryset=MeasurementQty.objects.all())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'phone', 'mobile', 'address', 'profile_image']
