from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import PantryItem
from .forms import LoginForm, AllergyDietForm, RecipeInformationForm, IngredientListForm
from django.urls import reverse


def login_view(request):
    form = LoginForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home'))
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid login')
        else:
            messages.error(request, 'Form data is not valid')

        # Pass the form to the context for both GET and POST requests
    return render(request, 'login.html', {'form': form})


def home(request):
    news_feed = [
        "News Item 1",
        "News Item 2",
        "News Item 3",
        # Add more news items as needed
    ]

    return render(request, 'home.html', {'news_feed': news_feed})


def create_recipe(request):
    allergy_diet_form = AllergyDietForm()
    recipe_info_form = RecipeInformationForm()
    ingredient_list_form = IngredientListForm()

    context = {
        'allergy_diet_form': allergy_diet_form,
        'recipe_info_form': recipe_info_form,
        'ingredient_list_form': ingredient_list_form,
    }
    return render(request, 'create_recipe.html')


def pantry(request):
    pantry_items = PantryItem.objects.all()
    context = {'pantry_items': pantry_items}
    return render(request, 'pantry.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def my_recipes(request):
    return render(request, 'my_recipes.html')


# Adds item to pantry
def add_item(request):
    if request.method == 'POST' and request.user.is_authenticated:
        item_name = request.POST.get('item_name')
        item_amount = request.POST.get('item_amount')

        if item_name and item_amount:
            pantry_item = PantryItem(user=request.user, item_name=item_name, item_amount=item_amount)
            pantry_item.save()

    return HttpResponseRedirect('/pantry')


# Clears the pantry
def clear_pantry(request):
    if request.user.is_authenticated:
        PantryItem.objects.filter(user=request.user).delete()
    return HttpResponseRedirect('/pantry')



def cart(request):
    return render(request, 'cart.html')
