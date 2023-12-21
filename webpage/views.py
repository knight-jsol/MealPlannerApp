# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from .models import PantryItem, Ingredients, RecipeIngredients, Recipes
from .forms import LoginForm, RecipeForm, RecipeIngredientForm
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import PantryItemForm
from django.views.decorators.http import require_POST
from .utils import generate_image
from django.shortcuts import get_object_or_404
from .nutrition_lookup import get_nutritional_data
from .forms import *
from .models import *
from django.contrib.auth import get_user_model, logout
from openai import OpenAI
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_view')  # Assumes you have a view named 'login'


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
    return render(request, 'home.html')  # Make sure 'home.html' is the template for the home page


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
    return render(request, 'pantry.html', {'pantry_items': pantry_items})


def forgot_password(request):
    return render(request, 'forgot_password.html')


def help(request):
    return render(request, 'help.html')


def my_recipes(request):
    return render(request, 'my_recipes.html')


def profile(request):
    try:
        # Fetch the user profile associated with the current user
        user_profile = UserProfile.objects.get(user=request.user)
        full_name = user_profile.full_name
    except UserProfile.DoesNotExist:
        # If the user profile does not exist, set full_name to None or a default value
        full_name = None

    return render(request, 'profile.html', {'full_name': full_name})



# Adds item to pantry


# views.py


def add_pantry_item(request):
    if request.method == 'POST':
        form = PantryItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)

            # Generate the image URL
            image_url = generate_image(new_item.name)
            if image_url:
                new_item.image_url = image_url

            # Get the nutritional data
            api_key = "V7DRp5nywS4bKNSbRdxkWE4niwwYSXJhYDTGY2oZ"
            food_item_name = new_item.name
            nutritional_data = get_nutritional_data(food_item_name, api_key)

            # Set the nutritional data fields
            new_item.protein = nutritional_data.get('Protein')
            new_item.cholesterol = nutritional_data.get('Cholesterol')
            new_item.energy = nutritional_data.get('Energy')
            new_item.carbohydrate = nutritional_data.get('Carbohydrate, by difference')

            new_item.save()
            return redirect('add_pantry_item')

    else:
        form = PantryItemForm()

    pantry_items = PantryItem.objects.all()
    return render(request, 'pantry.html', {'form': form, 'pantry_items': pantry_items})


# Clears the pantry
def clear_pantry(request):
    PantryItem.objects.all().delete()  # This deletes all PantryItem objects from the database
    return redirect('add_pantry_item')  # Redirect back to the pantry list page


def adjust_quantity(request, item_id):
    item = get_object_or_404(PantryItem, id=item_id)
    if request.method == 'POST':
        item.quantity = request.POST.get('quantity')
        item.save()
        return redirect('pantry')  # Redirect to the pantry page
    # Handle case for GET or other methods if needed


def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(PantryItem, id=item_id)
        item.delete()
        return redirect('pantry')  # Redirect to the pantry page


def cart(request):
    if request.method == 'POST':
        form = AddIngredientForm(request.POST)
        if form.is_valid():
            cart_item = form.save()
            cart, created = Cart.objects.get_or_create(pk=1)  # Get or create the Cart object
            cart.ingredients.add(cart_item)
    else:
        form = AddIngredientForm()

    cart, created = Cart.objects.get_or_create(pk=1)  # Get or create the Cart object
    cart_items = cart.ingredients.all()

    return render(request, 'cart.html', {'form': form, 'cart_items': cart_items})


def export_cart(request):
    cart, created = Cart.objects.get_or_create(pk=1)
    cart_items = cart.ingredients.all()

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="cart.txt"'

    for item in cart_items:
        response.write(f"{item.item_name} : {item.quantity}\n")

    return response


@login_required
def profile_edit(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form})
