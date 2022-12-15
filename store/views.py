from django.shortcuts import render, get_object_or_404
from categoryapp.models import Category
from store.models import Product
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def STORE(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by("-id")
        
        # Pagination Start
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        # Pagination End
        
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by("-id")
        
        # Pagination Start
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        # Pagination End


        product_count = products.count()

        

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def PRODUCT_DETAIL(request, category_slug, product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # Check item in cart exist or not
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }    
    return render(request, 'store/product_detail.html', context)


# Search Functionality
def SEARCH(request):
    products = Product.objects.order_by('-created_date')
    product_count = products.count()
    if request.method == 'GET':
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q (description__icontains=keyword)).order_by('-created_date')
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)