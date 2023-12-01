#forms.py
from io import BytesIO

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import PantryItem
from .utils import generate_image  # Assuming you have a generate_image function in utils.py
from urllib.request import urlopen
from django.core.files.base import ContentFile
from django.core.files import File
from .models import UserProfile


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


class AllergyDietForm(forms.Form):
    peanut_allergy = forms.BooleanField(required=False)
    dairy_allergy = forms.BooleanField(required=False)
    vegetarian = forms.BooleanField(required=False)
    vegan = forms.BooleanField(required=False)


class RecipeInformationForm(forms.Form):
    recipe_name = forms.CharField(max_length=100)
    ingredient_list = forms.CharField(max_length=500)
    instructions = forms.CharField(max_length=1000)
    prep_time = forms.CharField(max_length=50)
    cook_time = forms.CharField(max_length=50)


class IngredientListForm(forms.Form):
    base_ing = forms.CharField(max_length=100)
    # You can add more ingredient fields if necessary
    # However, dynamic addition of fields should be handled by JavaScript in the template


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'phone', 'mobile', 'address', 'profile_image']
