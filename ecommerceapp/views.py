from django.shortcuts import render, HttpResponse
from store.models import Product, ReviewRating

# Create your views here.

def Index(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    
    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    
    return render(request, 'home.html', context)