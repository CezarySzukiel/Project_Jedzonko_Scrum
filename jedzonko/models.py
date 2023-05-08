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


class Plan(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')


class DayName(models.Model):
    name = models.CharField(max_length=64)
    order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=64)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)
