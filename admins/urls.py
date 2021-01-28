from django.urls import path, include
from django.contrib.auth import views as auth_view

from .views import *

urlpatterns = [
    path('', index),
    path('index/', index, name="index"),
    # path('about/', About, name="about"),
    # path('contact/', Contact, name="contact"),
    # path('single-product/', SingleProduct, name="single-product"),
    # path('products/', Products, name="products"),
    # path('shopping-cart/', Cart, name="shopping-cart"),
    # path('checkout/', Checkout, name="checkout"),
    # path('wishlist/', Wishlist, name="wishlist"),
    # path('login-register/', LoginRegister, name="login-register"),
    path('sign-in/',
         auth_view.LoginView.as_view(template_name="atemplates/sign-in.html", redirect_authenticated_user=True),
         name="sign-in"),
    path('logout/', auth_view.LogoutView.as_view(), name="logout"),
    path('404/', notFound, name="404"),
    # Customers
    path('customers/', Customers.as_view(), name="customers"),
    path('edit-customer/', editCustomers, name="edit-customer"),
    # Products
    path('products-list/', allProducts, name="products-list"),
    path('add-products/', addProducts, name="add-products"),
    path('edit-products/', editProducts, name="edit-products"),
    # Categories
    path('categories-list/', AllCategories.as_view(), name="categories-list"),
    path('category-update/<int:pk>/', UpdateCategory.as_view(), name="update_category"),
    path('add-categories/', addCategories, name="add-categories"),
    path('edit-categories/', editCategories, name="edit-categories"),
    # Banners
    path('banners-list/', allBanner, name="banners-list"),
    path('add-banner/', addBanner, name="add-banner"),
    path('edit-banner/', editBanner, name="edit-banner"),
    # Orders
    path('confirmed-orders/', confirmedOrders, name="confirmed-orders"),
    path('packed-orders/', packedOrders, name="packed-orders"),
    path('out-for-delivered-orders/', outfordeliveredOrders, name="out-for-delivered-orders"),
    path('delivered-orders/', deliveredOrders, name="delivered-orders"),
    path('rejected-orders/', rejectedOrders, name="rejected-orders"),
]