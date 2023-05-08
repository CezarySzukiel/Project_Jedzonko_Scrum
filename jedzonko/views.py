from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        return render(request, "jedzonko/index.html")


class Dashboard(View):
    def get(self, request):
        # newestPlan = Plan.objects.all().ordered_by('created')[0]
        context = {
            'recipes': Recipe.objects.all().count(),
            # 'plans': Plan.objects.all().count(),
            # 'newestPlan': newestPlan,
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

