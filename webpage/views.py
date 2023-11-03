from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .models import CartItem

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
    pantry_items = request.COOKIES.get('pantry_items', '').split(',') if request.COOKIES.get('pantry_items') else []
    return render(request, 'pantry.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


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

