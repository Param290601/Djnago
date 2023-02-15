"""basics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home.as_view(), name = 'home'),
    path('product/',views.product.as_view(), name='product'),
    path('customer/<str:pk>/',views.customer.as_view(), name='customer'),
    path('create_order/',views.createOrder.as_view(), name='createOreder'),
    path('update_order/<str:pk>/',views.updateOrder.as_view(), name='updateOrder'),
    path('delete_order/<str:pk>/',views.deleteOrder.as_view(), name='deleteOrder'), 
    path('create_product/',views.createProduct.as_view(), name='createProduct'),
    path('update_product/<str:pk>/',views.updateProduct.as_view(), name='updateProduct'),
    path('delete_product/<str:pk>/',views.deleteProduct.as_view(), name='deleteProduct'), 
    path('register/',views.register.as_view(),name='register'),
    path('login/',views.loginpage.as_view(),name='login'),
    path('logout/',views.logoutUser.as_view(),name='logout'),
    path('user-page/',views.userpage.as_view(),name='user-page'),
    path('settings/',views.settings.as_view(),name='settings'),
    path('forgetpassword/',views.forgetpassword.as_view(),name = 'forgetpassword'),
    path('changepassword/<token>/',views.changepassword.as_view(), name = 'changepassword'),
    # path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name = 'password_reset_confirm'),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name = 'reset_password_complete'),

]
