from django.urls import path, include
from django.contrib.auth import views as auth_view

from .views import *

urlpatterns = [
    path('djrichtextfield/', include('djrichtextfield.urls')),
    path('', index, name="dashboard"),
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
    path('products-list/', AllProducts.as_view(), name="products_list"),
    path('add-products/', AddProducts.as_view(), name="add_products"),
    path('product-images/<int:pk>/', AddProductsImages, name="add_product_images"),
    path('edit-products/<int:pk>/', UpdateProducts.as_view(), name="update_products"),
    # ProductsClass
    path('product-class-list/', AllProductClass.as_view(), name="product_class_list"),
    path('add-product-class/', AddProductClass.as_view(), name="add_product_class"),
    path('edit-product-class/<int:pk>/', UpdateProductClass.as_view(), name="update_product_class"),
    # Categories
    path('categories-list/', AllCategories.as_view(), name="categories-list"),
    path('category-update/<int:pk>/', UpdateCategory.as_view(), name="update_category"),
    path('add-categories/', AddCategories.as_view(), name="add_categories"),
    path('delete-categories/<int:pk>/', DeleteCategory.as_view(), name="delete_categories"),
    # Orders
    path('orders-list/', AllOrders.as_view(), name="orders_list"),
    path('orders-update/<int:pk>/', UpdateOrders.as_view(), name="update_orders"),
    path('order-detail/<int:pk>/', DetailOrders.as_view(), name="detail_orders"),
    #customer
    path('customer-detail/<int:pk>/', DetailCustomer.as_view(), name="detail_customer"),
    path('customer-list/', ListCustomer.as_view(), name="list_customer"),
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