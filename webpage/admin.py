from django.contrib import admin
from .models import PantryItem, UserProfile, RecipesMade

admin.site.register(PantryItem)
admin.site.register(UserProfile)
admin.site.register(RecipesMade)