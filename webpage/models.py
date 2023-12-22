# models.py
from django.contrib.auth.models import User
from django.db import models


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


class RecipesMade(models.Model):
    title = models.TextField()  # Field definitions
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title

    # Add the Meta class inside the RecipesMade model
    class Meta:
        db_table = 'webpage_recipesmade'  # Explicitly set the table name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
