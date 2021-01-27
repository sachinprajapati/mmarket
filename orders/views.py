from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from .models import Address, OrderPayment
from .serializers import AddressSerializer, OrderPaymentSerializer

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

class CheckOutView(generics.CreateAPIView):
    serializer_class = OrderPaymentSerializer
    model = OrderPayment
    queryset = OrderPayment.objects.filter()