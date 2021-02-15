from django.shortcuts import render, get_object_or_404, Http404

from rest_framework import permissions, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import *
from .models import Maintance

class UserViewSet(generics.CreateAPIView):
	model = User
	queryset = model.objects.all()
	permission_classes = [permissions.AllowAny]
	serializer_class = UserCreateSerializer


class SendOTP(APIView):
	model = User
	queryset = model.objects.all()
	permission_classes = [permissions.AllowAny]

	def post(self, request, *args, **kwargs):
		data = request.data
		print("data is ", data)
		if not data.get('phone'):
			return Response({'phone': ["This field is required."]}, status=status.HTTP_404_NOT_FOUND)
		user = get_object_or_404(get_user_model(), phone=data['phone'])
		user.set_password('123456')
		user.save()
		return Response({'message': 'otp successfully sent, please enter otp'}, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):

	def post(self, request, *args, **kwargs):
	    data = request.data
	    if not data.get('phone') or not data.get('otp'):
	    	return Response({'phone': ["This field is required."], 'otp': ["This field is required."]}, status=status.HTTP_404_NOT_FOUND)
	    user = get_object_or_404(get_user_model(), phone=data['phone'])
	    if not user.check_password(data['otp']):
	    	return Response({'otp': 'Invalid otp entered'}, status=status.HTTP_400_BAD_REQUEST)
	    token, created = Token.objects.get_or_create(user=user)
	    return Response({
	        'token': token.key,
	        'user_id': user.pk,
	    })

class ProfileView(generics.RetrieveUpdateAPIView):
	model = User
	serializer_class = UserSerializer
	queryset = model.objects.all()

	def get_object(self):
		return self.request.user

class Downlines(generics.ListAPIView):
	model = User
	serializer_class = UserDownlineSerializer

	def get_object(self):
		return self.request.user

	def get_queryset(self):
		level = self.kwargs['level']
		if not level in range(1,11):
			raise Http404
		else:
			return self.request.user.get_downline(level)

class WalletHistoryView(generics.ListAPIView):
	model = WalletHistory
	serializer_class = WalletLogs

	def get_queryset(self):
		return self.model.objects.filter(wallet__user=self.request.user).order_by('-dt')

class DebugView(generics.RetrieveAPIView):
	model = Maintance

	def get_object(self):
		return self.model.objects.filter()[0].status if self.model.objects.filter().exists() else False