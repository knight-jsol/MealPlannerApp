from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Recipes

def home(request):
    news_feed = [
        "News Item 1",
        "News Item 2",
        "News Item 3",
        # Add more news items as needed
    ]

    return render(request, 'home.html', {'news_feed': news_feed})


def create_recipe(request):
    return render(request, 'create_recipe.html')

def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipes, recipe_id=recipe_id)
    return render(request, 'view_recipe.html', {'recipe': recipe})


def pantry(request):
    pantry_items = request.COOKIES.get('pantry_items', '').split(',') if request.COOKIES.get('pantry_items') else []
    return render(request, 'pantry.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')

def my_recipes(request):
    return render(request, 'my_recipes.html')


# Adds item to pantry
def add_item(request):
    item_name = request.POST.get('item_name', '')
    item_amount = request.POST.get('item_amount', '')

    if item_name and item_amount:
        pantry_items = request.COOKIES.get('pantry_items', '').split(',') if request.COOKIES.get('pantry_items') else []
        pantry_items.append((item_name, item_amount))
        response = render(request, 'pantry.html', {'pantry_items': pantry_items})
        response.set_cookie('pantry_items', ','.join([f'{item[0]}:{item[1]}' for item in pantry_items]))
        return response

    return HttpResponseRedirect('/pantry')


# Clears the pantry
def clear_pantry(request):
    response = HttpResponseRedirect('/pantry')
    response.delete_cookie('pantry_items')
    return response


def cart(request):
    return render(request, 'cart.html')

def lgoin(request):
    return render(request, 'login.html')


