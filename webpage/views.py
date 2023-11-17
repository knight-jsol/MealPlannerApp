from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import PantryItem
from .forms import LoginForm, AllergyDietForm, RecipeInformationForm, IngredientListForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import PantryItemForm
from django.views.decorators.http import require_POST
from .utils import generate_image




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

def profile(request):
    return render(request, 'profile.html')


# Adds item to pantry


def add_pantry_item(request):
    if request.method == 'POST':
        form = PantryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_pantry_item')  # Redirect to the same page to display the updated list

    else:
        form = PantryItemForm()

    pantry_items = PantryItem.objects.all()  # Fetch all pantry items
    return render(request, 'pantry.html', {'form': form, 'pantry_items': pantry_items})



# Clears the pantry
def clear_pantry(request):
    PantryItem.objects.all().delete()  # This deletes all PantryItem objects from the database
    return redirect('add_pantry_item')  # Redirect back to the pantry list page



def cart(request):
    return render(request, 'cart.html')
