from django.urls import path
from . import views

urlpatterns = [
    path('', views.STORE, name='store'),
    path('category/<slug:category_slug>/', views.STORE, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.PRODUCT_DETAIL, name='product_detail'),
    path('search/', views.SEARCH, name='search'),
    path('submit_review/<int:product_id>/', views.SubmitReview, name='submit_review'),
]