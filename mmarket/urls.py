from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', auth_view.LoginView.as_view(template_name="form_view.html", redirect_authenticated_user=True), name="login"),
    path('logout/', auth_view.LogoutView.as_view(), name="logout"),
    path('dashboard/', include('admins.urls')),
    path('api/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/', include('basket.urls')),
    path('api/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
