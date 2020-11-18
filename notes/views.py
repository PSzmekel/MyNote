from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from notes.serializers import NoteSerializer
from notes.models import Note


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Note.objects.all().order_by('created_date')
    serializer_class = NoteSerializer
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAuthenticated],
                                    'retrieve': [permissions.IsAuthenticated]}
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
