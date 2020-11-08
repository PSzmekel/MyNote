from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework.authtoken.views import obtain_auth_token

from accounts import urls as accountsUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(accountsUrls)),
    path('auth/', obtain_auth_token)

]
