from django.shortcuts import render, HttpResponse
from store.models import Product

# Create your views here.

def Index(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    
    return render(request, 'home.html', context)