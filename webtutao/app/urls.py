from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('product/', views.product, name = 'product'),
    path('update_item/', views.update_item, name = 'update_item'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('search/', views.search, name = 'search'),
    path('register/', views.register, name = 'register'),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('category/', views.category, name = 'category'),
    path('detail/', views.detail, name = 'detail'),
]
