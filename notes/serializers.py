from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'topic', 'text', 'created_date', 'last_edit', 'owner']
        read_only_fields = ['id', 'created_date', 'last_edit']


class NoteUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['topic', 'text']


class NoteMiniSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'topic', 'text', 'last_edit']
