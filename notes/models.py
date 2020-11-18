from django.db import models
from django.conf import settings
from uuid import uuid4
from django.db import IntegrityError

from random import choice
from string import ascii_lowercase


class Note(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=8)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes',
                              on_delete=models.CASCADE)
    topic = models.CharField(max_length=30)
    text = models.TextField(max_length=4092, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        def _get_random_string(length):
            letters = ascii_lowercase
            result_str = ''.join(choice(letters) for i in range(length))
            return result_str

        if not self.id:
            self.id = _get_random_string(8)
            # using your function as above or anything else
        success = False
        failures = 0
        while not success:
            try:
                super(Note, self).save(*args, **kwargs)
            except IntegrityError:
                failures += 1
                if failures > 5:  # or some other arbitrary cutoff point at which things are clearly wrong
                    raise
                else:
                    # looks like a collision, try another random value
                    self.id = _get_random_string(8)
            else:
                success = True
