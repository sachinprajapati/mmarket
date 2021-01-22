from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets

from .models import Address
from .serializers import AddressSerializer

class AddressView(viewsets.ModelViewSet):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Address.objects.filter(user=self.request.user, pk=self.kwargs['pk'])
        if self.request.method == 'POST':
            return self
        if self.request.method == 'GET':
            return Address.objects.filter(user=self.request.user)