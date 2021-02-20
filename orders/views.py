from django.shortcuts import render, get_object_or_404
from django.db.models import Sum

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Address, OrderPayment, Orders, OrderItems
from basket.models import CartLine
from admins.models import AvailableAddress
from .serializers import *

class AddressView(viewsets.ModelViewSet):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    # def list(self, request):
    #     qt = self.model.objects.filter(user=request.user)
    #     return Response(AddressSerializer(qt, many=True).data, status=status.HTTP_200_OK)
    #
    # def retrieve(self, request, pk=None):
    #     qt = get_object_or_404(self.queryset, pk=pk, user=request.user)
    #     return Response(AddressSerializer(qt).data, status=status.HTTP_200_OK)

class CheckOutView(APIView):
    serializer_class = OrdersSerializer
    model = OrderPayment
    queryset = OrderPayment.objects.filter()

    def get(self, request, *args, **kwargs):
        items = CartLine.objects.filter(cart=request.user.cart)
        if not items.exists():
            return Response({"error": "No item selected to checkout"}, status=status.HTTP_404_NOT_FOUND)
        return Response(items.aggregate(Sum('price')), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(request.user)
        items = CartLine.objects.filter(cart=request.user.cart)
        if not data.get("address"):
            return Response({"address": ["This field is required"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not Address.objects.filter(pk=data["address"], user=request.user).exists():
                return Response({"address": "invalid address"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                add = Address.objects.get(pk=data["address"], user=request.user)
                if not AvailableAddress.objects.filter(pincode=add.pincode).exists():
                    return Response({'pincode': 'no delivery at this pincode'}, status=status.HTTP_400_BAD_REQUEST)
        if not items.exists():
            return Response({"error": "No item selected to checkout"}, status=status.HTTP_404_NOT_FOUND)
        if not data.get("type"):
            return Response({"type": ["no payment method selected"]})
        else:
            if data['type'] != 1:
                return Response({"type": "invalid payment"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                d = {"customer": request.user.pk, "address": data["address"], "amount":items.aggregate(Sum('price'))['price__sum']}
                order = OrdersSerializer(data=d)
                if not order.is_valid():
                    return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    amount = items.aggregate(Sum('price'))['price__sum']
                    print("amount is", amount)
                    order.save()
                    try:
                        op = OrderPayment(order_id=order.data['id'], amount=amount, type=data['type'])
                        op.save()
                    except Exception as e:
                        print(e)
                    return Response(order.data, status=status.HTTP_201_CREATED)
        # if not data.get("amount"):
        #     return Response({"type": ["no paid amount found"]})
        # else:
        #     if items.aggregate(Sum('price')).get('price__sum', 0) != data['amount']:
        #         return Response({'amount': ['wrong amount selected']}, status=status.HTTP_400_BAD_REQUEST)

class OrdersView(viewsets.ModelViewSet):
    model = Orders
    serializer_class = OrdersListSerializer
    queryset = Orders.objects.filter()

    def list(self, request):
        queryset = Orders.objects.filter(customer=request.user).order_by("-dt")
        serializer = OrdersListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Orders.objects.filter(customer=request.user)
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

class PincodeAvailView(generics.RetrieveAPIView):
    model = AvailableAddress
    serializer_class = AvailableAddressSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        print(self.kwargs)
        obj = get_object_or_404(AvailableAddress, pincode=self.kwargs['pincode'])
        return obj

class TrackOrder(generics.RetrieveAPIView):
    model = Orders
    serializer_class = TrackOrderSerializer
    queryset = Orders.objects.filter()

    def get_object(self):
        return get_object_or_404(Orders, pk=self.kwargs['pk'], customer=self.request.user)

class CancelOrder(generics.CreateAPIView):
    model = OrderStatus
    serializer_class = CancelOrderSerializer
    queryset = OrderStatus.objects.filter()

    def get_object(self):
        return get_object_or_404(Orders, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        print(self.request.user)
        order = get_object_or_404(Orders, pk=self.kwargs['pk'], customer=self.request.user)
        print("order is", order)
        if order.get_Status()>1:
            return Response({"status": ["can't cancel this order"]}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CancelOrderSerializer(data={'order': order.pk, 'status':6})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
