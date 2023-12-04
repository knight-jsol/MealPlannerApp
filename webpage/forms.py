from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Recipes, Ingredients, MeasurementUnits, MeasurementQty


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


class JulianDateForm(forms.Form):
    julian_date = forms.IntegerField(label='Julian Date', min_value=0)


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
