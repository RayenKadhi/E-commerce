from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('store/', views.main, name='main'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('processOrder/', views.processOrder, name='processOrder'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('logoutPage/', views.logoutPage, name='logoutPage'),
]