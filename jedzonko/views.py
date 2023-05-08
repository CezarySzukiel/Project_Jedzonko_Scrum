import random

from django.shortcuts import render
from django.views import View
from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        recipes = []
        for recipe in Recipe.objects.all():
            recipes.append([recipe.name, recipe.description])
        random.shuffle(recipes)

        names = [i[0] for i in recipes[:3]]
        descriptions = [i[1] for i in recipes[:3]]

        return render(request, "jedzonko/index.html", {'names': names,
                                                       'descriptions': descriptions})


class Dashboard(View):
    def get(self, request):
        return render(request, "jedzonko/dashboard.html")
