from django.contrib import admin
from .models import *

admin.site.register(PantryItem)
admin.site.register(Recipes)
admin.site.register(CalendarTracker)
admin.site.register(Users)
admin.site.register(Roles)

