#models.py
from django.contrib.auth.models import User
from django.db import models
from capstone import settings


class PantryItem(models.Model):
    image_url = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='pantry_images/', blank=True, null=True)
    protein = models.FloatField(null=True, blank=True)
    cholesterol = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    carbohydrate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}"


class Roles(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=30)
    role_desc = models.CharField(max_length=1000)


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    role_id = models.ForeignKey("Roles", on_delete=models.CASCADE)
    user_pass = models.CharField(max_length=50)


class Recipes(models.Model):
    recipe_id = models.IntegerField(primary_key=True)
    recipe_name = models.CharField(max_length=200)
    recipe_desc = models.CharField(max_length=10000)
    recipe_ingredients = models.CharField(max_length=500)  # ignore this
    recipe_preptime = models.IntegerField()  # Temp value, in minutes
    recipe_cooktime = models.IntegerField()  # Temp value, in minutes
    recipe_peanut = models.BooleanField(default=False)  # Flag for peanut allergy
    recipe_Dairy = models.BooleanField(default=False)  # Flag for dairy allergy
    recipe_vegetarian = models.BooleanField(default=False)  # Flag for vegetarian preference
    recipe_vegan = models.BooleanField(default=False)  # Flag for vegan preference
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ingredients(models.Model):
    food = models.CharField(max_length=100)
    measure = models.CharField(max_length=100)
    grams = models.IntegerField()
    calories = models.IntegerField()
    fat = models.CharField(max_length=10)
    sat_fat = models.CharField(max_length=10)
    fiber = models.CharField(max_length=10)
    carbs = models.CharField(max_length=10)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.food


class MeasurementUnits(models.Model):
    unit_id = models.IntegerField(primary_key=True)
    measurement_desc = models.CharField(max_length=500)


class MeasurementQty(models.Model):
    qty_id = models.IntegerField(primary_key=True)
    qty_desc = models.CharField(max_length=200)


class RecipeIngredients(models.Model):
    recipe_ingredient_id = models.IntegerField(primary_key=True)
    recipe_id = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    unit_id = models.ForeignKey("MeasurementUnits", on_delete=models.CASCADE)
    qty_id = models.ForeignKey("MeasurementQty", on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey("Ingredients", on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
