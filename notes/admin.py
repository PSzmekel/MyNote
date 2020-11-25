from django.contrib import admin

from notes.models import Note


class NoteAdmin(admin.ModelAdmin):
    fields = ['id', 'owner', 'topic', 'text']


admin.site.register(Note, NoteAdmin)
