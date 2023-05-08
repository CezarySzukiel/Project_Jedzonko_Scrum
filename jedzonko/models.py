from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    # ingredients = models.ManyToManyField(Ingredients)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField()
