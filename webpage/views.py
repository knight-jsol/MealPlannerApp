from django.shortcuts import render, HttpResponse

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
    return render(request, 'pantry.html')


def cart(request):
    return render(request, 'cart.html')