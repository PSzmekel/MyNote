from rest_framework import viewsets
from notes.serializers import NoteSerializer
from notes.models import Note


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Note.objects.all().order_by('created_date')
    serializer_class = NoteSerializer
    #permission_classes = [permissions.IsAuthenticated]
