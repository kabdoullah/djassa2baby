import uuid
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.label = self.label.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Rôle"

    def __str__(self):
        return self.label
