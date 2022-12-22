from django.shortcuts import render, redirect, get_object_or_404
from categoryapp.models import Category
from store.models import Product, ReviewRating
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import ReviewForms
from django.contrib import messages
from orders.models import OrderProduct

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

    # Check order Product exist or not by Submit Review
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    
    else:
        orderproduct = None
    # End Review Check

    # Get the Review
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    # End get the Review

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
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


# Submit The Review
def SubmitReview(request, product_id):
    
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank ypu! Your review has been updated.')
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
             form = ReviewForms(request.POST)
             if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank ypu! Your review has been submitted.')
                return redirect(url)




