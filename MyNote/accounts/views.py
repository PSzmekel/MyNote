from rest_framework import viewsets
from rest_framework import permissions
from MyNote.accounts.serializers import CustomUserSerializer
from MyNote.accounts.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    #permission_classes = [permissions.IsAuthenticated]
