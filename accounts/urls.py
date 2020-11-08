from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
