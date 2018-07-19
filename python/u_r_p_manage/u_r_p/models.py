from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    node_id = models.CharField(max_length=30, null=True)
    department = models.CharField(max_length=30, null=True)
    position = models.CharField(max_length=30, null=True)

    class Meta(AbstractUser.Meta):
        pass