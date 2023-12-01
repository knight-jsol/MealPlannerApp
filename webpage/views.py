from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from .models import PantryItem, Ingredients, RecipeIngredients, Recipes
from .forms import LoginForm, RecipeForm, RecipeIngredientForm
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid login')
        else:
            print(form.errors)
            messages.error(request, 'Form data is not valid')
    else:
        form = LoginForm()

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
    # Get the user's pantry items (ingredient IDs)
    user_pantry_item_ids = PantryItem.objects.filter(user=request.user).values_list('item_name', flat=True)

    # Get all recipes and their ingredients
    all_recipes = Recipes.objects.all()
    recipe_ingredient_pairs = RecipeIngredients.objects.filter(recipe_id__in=all_recipes).values_list('recipe_id',
                                                                                                      'ingredient_id')

    # Count matching ingredients for each recipe
    recipe_match_counts = defaultdict(int)
    for recipe_id, ingredient_id in recipe_ingredient_pairs:
        if ingredient_id in user_pantry_item_ids:
            recipe_match_counts[recipe_id] += 1

    # Sort recipes by the number of matching ingredients
    sorted_recipes = sorted(recipe_match_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Fetch the recipe details for the top matching recipes
    top_recipes = [Recipes.objects.get(id=recipe_id) for recipe_id, _ in sorted_recipes]

    # Prepare final data to pass to the template
    recipe_details = [{'recipe': recipe, 'matching_ingredients': recipe_match_counts[recipe.id]} for recipe in
                      top_recipes]

    return render(request, 'create_recipe.html', {'recipe_details': recipe_details})


def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user_id = request.user  # assuming you have a user model
            recipe.save()

            # Process dynamic ingredient fields
            ingredient_names = request.POST.getlist('ingredient_name[]')
            units = request.POST.getlist('unit[]')
            quantities = request.POST.getlist('quantity[]')

            for name, unit, quantity in zip(ingredient_names, units, quantities):
                RecipeIngredients.objects.create(
                    recipe_id=recipe,
                    ingredient_id=name,
                    unit_id=unit,
                    qty_id=quantity
                )

            return redirect('some_view')  # Redirect to a desired page

    else:
        recipe_form = RecipeForm()

    ingredients = Ingredients.objects.all()
    return render(request, 'add_recipe.html', {
        'recipe_form': recipe_form,
        'ingredients': ingredients
    })


def pantry(request):
    pantry_items = PantryItem.objects.all()
    context = {'pantry_items': pantry_items}
    return render(request, 'pantry.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def help(request):
    return render(request, 'help.html')


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
