from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import login_view as custom_user_login

urlpatterns = [
    path("", custom_user_login, name="login_view"),
    path("create_recipe", views.create_recipe, name="create_recipe"),
    path("pantry", views.pantry, name="pantry"),
    path("cart", views.cart, name="cart"),
    path('add_item/', views.add_item, name='add_item'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('clear_pantry/', views.clear_pantry, name='clear_pantry'),
    path('home', views.home, name='home'),
    path('my_recipes', views.my_recipes, name='my_recipes'),
]