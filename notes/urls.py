from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers
from notes import views

router = routers.DefaultRouter()
router.register(r'notes', views.NoteViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
