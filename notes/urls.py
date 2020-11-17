from django.conf.urls import url, include
from rest_framework import routers
from notes import views

router = routers.DefaultRouter()
router.register(r'notes', views.NoteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
