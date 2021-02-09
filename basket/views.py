from django.shortcuts import render, get_object_or_404, Http404
from rest_framework import permissions, status, viewsets, generics
from rest_framework.response import Response

from .models import Cart, CartLine
from products.models import Product
from .serializers import AddCartSerializer, ListCartSerializer

class CartViewSet(viewsets.ViewSet):
    queryset = CartLine.objects.all()

    def list(self, request):
        queryset = CartLine.objects.filter(cart=request.user.cart)
        serializer = ListCartSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data.update({"cart": request.user.cart.id})
        serializer = AddCartSerializer(data=data)
        if serializer.is_valid():
            if CartLine.objects.filter(cart=request.user.cart, product__id=data['product']).exists():
                return Response({"product": ["product already exists"]}, status=status.HTTP_400_BAD_REQUEST)
            product = get_object_or_404(Product, pk=data['product'])
            if not hasattr(product, 'stockrecord'):
                return Response({"product": ["product out of stock"]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not product.stockrecord.get_available(data.get('quantity', 1)):
                    return Response({"product": ["product not available"]}, status=status.HTTP_400_BAD_REQUEST)
            print("data is", data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        data = request.data
        if not data.get('quantity'):
            return Response({"quantity": "Must Enter Quantity"}, status=status.HTTP_400_BAD_REQUEST)
        if not product.stockrecord.get_available(data.get('quantity', 1)):
            return Response({"product": ["product not available"]}, status=status.HTTP_400_BAD_REQUEST)
        cl = get_object_or_404(CartLine, product=product, cart=request.user.cart)
        serializer = ListCartSerializer(cl, data={'quantity': data['quantity']}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(CartLine, product_id=kwargs['pk'], cart=request.user.cart)
            instance.delete()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
