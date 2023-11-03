from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


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
