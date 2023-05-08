from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        return render(request, "jedzonko/index.html")


class Dashboard(View):
    def get(self, request):
        return render(request, "jedzonko/dashboard.html")


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

