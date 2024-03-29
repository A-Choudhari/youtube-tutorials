from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_active = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    gender = models.IntegerField(default=0)


