from django.db import models


class PantryItem(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_amount = models.IntegerField()


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
    recipe_ingredients = models.CharField(max_length=10000)  # Temp value
    recipe_preptime = models.IntegerField()  # Temp value, in minutes
    recipe_cooktime = models.IntegerField()  # Temp value, in minutes
    recipe_peanut = models.BooleanField(default=False)
    recipe_Dairy = models.BooleanField(default=False)
    recipe_vegetarian = models.BooleanField(default=False)
    recipe_vegan = models.BooleanField(default=False)
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE)


class Ingredients(models.Model):
    ingredient_id = models.IntegerField(primary_key=True)
    food = models.CharField(max_length=100)
    measure = models.CharField(max_length=100)
    grams = models.IntegerField()
    calories = models.IntegerField()
    fat = models.IntegerField()
    sat_fat = models.IntegerField()
    fiber = models.IntegerField()
    carbs = models.IntegerField()
    category = models.CharField(max_length=100)


class MeasurementUnits(models.Model):
    unit_id = models.IntegerField(primary_key=True)
    measurement_desc = models.CharField(max_length=500)


class MeasurementQty(models.Model):
    qty_id = models.IntegerField(primary_key=True)
    qty_desc = models.CharField(max_length=200)


class RecipeIngredients(models.Model):
    recipe_id = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    unit_id = models.ForeignKey("MeasurementUnits", on_delete=models.CASCADE)
    qty_id = models.ForeignKey("MeasurementQty", on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey("Ingredients", on_delete=models.CASCADE)
