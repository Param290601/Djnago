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

urlpatterns = [
    path('',views.home, name = 'home'),
    path('product/',views.prodcut, name='product'),
    path('customer/<str:pk>/',views.customer, name='customer'),
    path('create_order/',views.createOrder, name='createOreder'),
    path('update_order/<str:pk>/',views.updateOrder, name='updateOrder'),
    path('delete_order/<str:pk>/',views.deleteOrder, name='deleteOrder'),
    path('register/',views.register,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutUser,name='logout'),

]
