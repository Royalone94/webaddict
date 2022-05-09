"""webaddict URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .custom_jwt_serializer import CustomJWTSerializer
from .views import (
    UserList
)
from .views import *

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movies")
router.register(r"tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path('auth-jwt/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
    path('auth-jwt-refresh/', refresh_jwt_token),
    path('auth-jwt-verify/', verify_jwt_token),
    path('users/', UserList.as_view()),
    path('', include(router.urls)),
]