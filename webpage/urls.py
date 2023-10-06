from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("/create_recipe", views.create_recipe, name="create_recipe"),
    path("/pantry", views.pantry, name="pantry"),
    path("/cart", views.cart, name="cart")
]