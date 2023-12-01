from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("create_recipe", views.create_recipe, name="create_recipe"),
    path("pantry", views.pantry, name="pantry"),
    path("cart", views.cart, name="cart"),
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_item/', views.add_item, name='add_item'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('clear_pantry/', views.clear_pantry, name='clear_pantry'),
    path('home', views.home, name='home'),
    path('my_recipes', views.my_recipes, name='my_recipes'),
    path('calendar', views.calendar, name='calendar'),
]