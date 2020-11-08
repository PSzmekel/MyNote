from django.contrib import admin
from django.urls import path

from django.conf.urls import include
from accounts import urls as accountsUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(accountsUrls)),
]
