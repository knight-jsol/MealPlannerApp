# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
                  path("", views.login_view, name="login_view"),
                  path("create_recipe", views.create_recipe, name="create_recipe"),
                  path("pantry", views.pantry, name="pantry"),
                  path("cart", views.cart, name="cart"),
                  path('add_pantry_item/', views.add_pantry_item, name='add_pantry_item'),
                  path('forgot_password/', views.forgot_password, name='forgot_password'),
                  path('clear_pantry/', views.clear_pantry, name='clear_pantry'),
                  path('home', views.home, name='home'),
                  path('my_recipes', views.my_recipes, name='my_recipes'),
                  path('profile', views.profile, name='profile'),
                  path('adjust_quantity/<int:item_id>/', views.adjust_quantity, name='adjust_quantity'),
                  path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
                  path('profile_edit/', views.profile_edit, name='profile_edit'),
                  path('export_cart/', views.export_cart, name='export_cart'),
                  path('logout/', views.logout_view, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
