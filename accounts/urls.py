from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.REGISTER, name='register'),
    path('login/', views.LOGIN, name='login'),
    path('logout/', views.LOGOUT, name='logout'),
    path('dashboard/', views.DASHBOARD, name='dashboard'),
    path('', views.DASHBOARD, name='dashboard'),
    # Activate Email
    path('activate/<uidb64>/<token>/', views.ACTIVATE, name='activate'),
    # Forgot Password
    path('forgotPassword/', views.FORGOTPASSWORD, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.ResetpasswordValidate, name='resetpassword_validate'),
    path('resetPassword/', views.ResetPassword, name='resetPassword'),
    
]