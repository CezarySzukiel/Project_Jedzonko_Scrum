from django.db import models
from django.template.defaultfilters import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    preparation_method = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')

    def __str__(self):
        return self.name


class DayName(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

    def __str__(self):
        return self.meal_name


class Page(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



