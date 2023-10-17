from django.db import models
from rest_framework.settings import settings

# Create your models here.


class Ingredient(models.Model):
    """Models for ingredients"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
