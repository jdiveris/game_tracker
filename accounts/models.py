from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=12, blank=True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.username
        super().save(*args, **kwargs)
