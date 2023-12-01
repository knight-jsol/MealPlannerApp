from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
from .forms import LoginForm, JulianDateForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid login')
    else:
        form = LoginForm()
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


# Next 3 functions are all atrocious code
def cart(request):
    cart = request.session.get('cart', {})
    items = Item.objects.filter(id__in=cart.keys())
    return render(request, 'cart.html', {'cart': cart, 'items': items})

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
    request.session['cart'] = cart
    return redirect('cart_detail')
# surely I will replace this before the end of semester :clueless:


def lgoin(request):
    return render(request, 'login.html')

def calendar(request):
    if request.method == 'POST' and ('breakfast_recipe_id' in request.POST or 
        'dinner_recipe_id' in request.POST or 'lunch_recipe_id' in request.POST):
        # This block handles the recipe update form
        julian_date = request.POST.get('julianDay')
        tracker = get_object_or_404(CalendarTracker, julianDay=julian_date, year=2023)

        breakfast_id = request.POST.get('breakfast_recipe_id')
        lunch_id = request.POST.get('lunch_recipe_id')
        dinner_id = request.POST.get('dinner_recipe_id')

        if breakfast_id:
            tracker.breakfast_recipe = Recipes.objects.get(pk=breakfast_id)
        if lunch_id:
            tracker.lunch_recipe = Recipes.objects.get(pk=lunch_id)
        if dinner_id:
            tracker.dinner_recipe = Recipes.objects.get(pk=dinner_id)
        
        tracker.save()
        return render(request, 'calendar.html', {'tracker': tracker})
    elif request.method == 'POST':
        form = JulianDateForm(request.POST)
        if form.is_valid():
            julian_date = form.cleaned_data['julian_date']
            tracker, created = CalendarTracker.objects.get_or_create(julianDay=julian_date, defaults={'year': 2023})
            if created:
                # Perform additional actions if needed when a new record is created
                pass

            return render(request, 'calendar.html', {'tracker': tracker})
    else:
        form = JulianDateForm()

    return render(request, 'calendar_form.html', {'form': form})
    

    