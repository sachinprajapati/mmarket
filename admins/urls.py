from django.urls import path, include
from django.contrib.auth import views as auth_view

from .views import *

urlpatterns = [
    path('djrichtextfield/', include('djrichtextfield.urls')),
    path('', index, name="dashboard"),
    path('index/', index, name="index"),
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
    path('add-stock/<int:pk>/', AddProductStock.as_view(), name="product_stock"),
    path('update-stock/<int:pk>/', UpdateProductStock.as_view(), name="update_stock"),
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
    path('orders-status/<int:pk>/', UpdateOrders.as_view(), name="update_orders"),
    path('order-detail/<int:pk>/', DetailOrders.as_view(), name="detail_orders"),
    #customer
    path('customer-detail/<int:pk>/', DetailCustomer.as_view(), name="detail_customer"),
    path('customer-list/', ListCustomer.as_view(), name="list_customer"),
    # Banners
    path('banners-list/', AllBanner.as_view(), name="banners_list"),
    path('add-banner/', AddBanner.as_view(), name="add_banner"),
    path('update-banner/<int:pk>/', UpdateBanner.as_view(), name="update_banner"),
    # pincode
    path('pincode-list/', PincodeList.as_view(), name="pincode_list"),
    path('add-pincode/', AddPincode.as_view(), name="add_pincode"),
    path('update-pincode/<int:pk>/', UpdatePincode.as_view(), name="update_pincode"),
    #Maintance
    path('update-status/', UpdateDebug.as_view(), name="debug"),
    # Orders
    # path('confirmed-orders/', confirmedOrders, name="confirmed-orders"),
    # path('packed-orders/', packedOrders, name="packed-orders"),
    # path('out-for-delivered-orders/', outfordeliveredOrders, name="out-for-delivered-orders"),
    # path('delivered-orders/', deliveredOrders, name="delivered-orders"),
    # path('rejected-orders/', rejectedOrders, name="rejected-orders"),
    #coupons
    path('add-coupon/', AddCouponView.as_view(), name="add_coupon"),
    path('coupon-list/', ListCouponView.as_view(), name="coupon_list"),
    path('coupon-update/<int:pk>/', UpdateCouponView.as_view(), name="coupon_update"),
    path('coupon-detail/<int:pk>/', DetailCouponView.as_view(), name="coupon_detail"),
]