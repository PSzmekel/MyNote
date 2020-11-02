from django.conf.urls import url, include
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
