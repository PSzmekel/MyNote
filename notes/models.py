from django.db import models
from django.conf import settings
from uuid import uuid4
from django.db import IntegrityError


class Note(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=8)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    topic = models.CharField(max_length=30)
    text = models.TextField(max_length=4092, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id:
            super(Note, self).save(*args, **kwargs)
            return

        unique = False
        while not unique:
            try:
                self.id = uuid4().hex
                super(Note, self).save(*args, **kwargs)
            except IntegrityError:
                self.id = uuid4().hex
            else:
                unique = True
