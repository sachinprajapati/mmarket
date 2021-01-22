from rest_framework import serializers

from .models import Cart, CartLine

from products.serializers import ListProductSerializer

class AddCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartLine
        fields = ('product', 'quantity', 'cart')
        # fields = "__all__"

class ListCartSerializer(serializers.ModelSerializer):
    product = ListProductSerializer(read_only=True)
    class Meta:
        model = CartLine
        fields = ('product', 'quantity', 'price')

# class UpdateCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartLine
#         fields = ('prouct', 'quantity')

