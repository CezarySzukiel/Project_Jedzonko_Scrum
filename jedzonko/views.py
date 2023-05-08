from django.http import HttpResponse
import random

from django.shortcuts import render
from django.views import View
from jedzonko.models import *


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
        newest_plan = Plan.objects.all().order_by('created').first()
        context = {
            'recipes': Recipe.objects.all().count(),
            'plans': Plan.objects.all().count(),
            'newestPlan': newest_plan,
        }
        return render(request, "jedzonko/dashboard.html", context)



class RecipeView(View):
    def get(self, request):
        return HttpResponse("Tu będzie widok przepisu")


# class RecipeList(View):
# def get(self, request):
#    return HttpResponse("Tu będzie lista przepisów")


class AddRecipe(View):
    def get(self, request):
        return HttpResponse("Tu będzie dodawanie jednego przepisu")


class ModifyRecipe(View):
    def get(self, request):
        return HttpResponse("Tu będzie modyfikacja przepisu")


class PlanList(View):
    def get(self, request):
        return HttpResponse("Tu będzie lista planów")


class AddPlan(View):
    def get(self, request):
        return HttpResponse("Tu będzie dodawanie nowego planu")


class AddRecipeToPlan(View):
    def get(self, request):
        return HttpResponse("Tu będzie dodawanie przepisu do planu")


def recipe(request):
    return render(request, 'jedzonko/app-recipes.html')

