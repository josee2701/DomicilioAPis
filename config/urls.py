"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from accounts.views import ClientViewSet, DriverViewSet
from locations.views import AddressViewSet
from services.views import ServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'services', ServiceViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # Fallback: cualquier URL que no matchee arriba
    re_path(r'^.*$', RedirectView.as_view(
        url='/api/',  
        permanent=False           
    ), name='fallback'),
]
