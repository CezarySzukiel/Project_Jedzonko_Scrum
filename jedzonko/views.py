from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        return render(request, "jedzonko/index.html")


class Dashboard(View):
    def get(self, request):
        context = {
            'recipes': Recipe.objects.all().count(),
            # 'plans': Plan.objects.all().count()
        }
        return render(request, "jedzonko/dashboard.html", context)
        


class RecipeView(View):
   def get(self, request, id):
        return HttpResponse("Tu będzie widok przepisu")


# class RecipeList(View):
  # def get(self, request):
    #    return HttpResponse("Tu będzie lista przepisów")


class AddRecipe(View):
    def get(self, request):
        return HttpResponse("Tu będzie dodawanie jednego przepisu")


class ModifyRecipe(View):
    def get(self, request, id):
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
    recipes_list = Recipe.objects.all().order_by('-votes', 'created')
    paginator = Paginator(recipes_list, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'jedzonko/app-recipes.html', {'page_obj': page_obj})
