from rest_framework import serializers

from .models import Cart, CartLine, WishList

from products.serializers import ListProductSerializer

class AddCartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1)
    class Meta:
        model = CartLine
        fields = ('product', 'quantity', 'cart', 'wishlist')
        # fields = "__all__"

class ListCartSerializer(serializers.ModelSerializer):
    product = ListProductSerializer(read_only=True)
    class Meta:
        model = CartLine
        fields = ('product', 'quantity', 'price')

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('product', 'user')