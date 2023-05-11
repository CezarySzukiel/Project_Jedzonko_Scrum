from django.core.paginator import Paginator
from django.http import HttpResponse
import random

from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        if Recipe.objects.all().count() > 0:
            recipes = []
            for my_recipe in Recipe.objects.all():
                recipes.append([my_recipe.name, my_recipe.description])
            random.shuffle(recipes)

            names = [i[0] for i in recipes[:3]]
            descriptions = [i[1] for i in recipes[:3]]

            return render(request, "jedzonko/index.html", {'names': names,
                                                           'descriptions': descriptions,
                                                           'Recipes': "true"})
        else:
            return render(request, "jedzonko/index.html", {'lackOfRecipes': "Chwilowo brak przepisów :("})


class Dashboard(View):
    def get(self, request):
        if Plan.objects.all().count() > 0:
            newest_plan = Plan.objects.all().order_by('-id').first()
            context = {
                'recipes': Recipe.objects.all().count(),
                'plans': Plan.objects.all().count(),
                'newestPlan': newest_plan,
                'recipePlan': RecipePlan.objects.filter(plan_id=newest_plan.id),
                'days': DayName.objects.filter(recipeplan__plan_id=newest_plan.id).distinct(),
            }
            return render(request, "jedzonko/dashboard.html", context)
        else:
            context = {
                'recipes': Recipe.objects.all().count(),
                'plans': Plan.objects.all().count(),
            }
            return render(request, "jedzonko/dashboard.html", context)


class RecipeView(View):
    def get(self, request, id_):
        my_recipe = Recipe.objects.get(pk=id_)
        # splitting by enters and removing double enters
        preparation = [i for i in my_recipe.preparation_method.split("\n") if i and i != '\r']
        ingredients = [i for i in my_recipe.ingredients.split("\n") if i and i != '\r']
        print(preparation)
        return render(request, 'jedzonko/app-recipe-details.html',
                      {'recipe': my_recipe,
                       'preparation': preparation,
                       'ingredients': ingredients})


class AddRecipe(View):
    def get(self, request):
        return render(request, 'jedzonko/app-add-recipe.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        time = request.POST.get('time')

        preparation = request.POST.get('preparation')
        ingredients = request.POST.get('ingredients')

        if not (name and description and time and preparation and ingredients):
            return render(request, 'jedzonko/app-add-recipe.html',
                          {'message': 'Musisz uzupełnić wszystkie pola'})

        try:
            time = int(time)
        except ValueError:
            return render(request, 'jedzonko/app-add-recipe.html',
                          {'message': 'Czas przygotowania musi być liczbą całkowitą'})

        if time < 1:
            return render(request, 'jedzonko/app-add-recipe.html',
                          {'message': 'Minimalny czas przygotowania to jedna minuta'})

        Recipe.objects.create(name=name, description=description,
                              preparation_time=time, preparation_method=preparation,
                              ingredients=ingredients)

        return redirect('recipe')


class ModifyRecipe(View):
    def get(self, request, id):
        return HttpResponse("Tu będzie modyfikacja przepisu")


class PlanList(View):
    def get(self, request):
        if Plan.objects.all().count() > 0:
            plan_list = Plan.objects.all().order_by('name')
            paginator = Paginator(plan_list, 50)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(request, 'jedzonko/app-schedules.html', {'page_obj': page_obj})
        else:
            return render(request, 'jedzonko/app-schedules.html', {'lackOfPlans': "Chwilowo brak planów :("})


class AddPlan(View):
    def get(self, request):
        return render(request, 'jedzonko/app-add-schedules.html')

    def post(self, request):
        name = request.POST.get("planName")
        desc = request.POST.get("planDescription")
        if not (name and desc):
            return render(request, 'jedzonko/app-add-schedules.html',
                          {'message': f'Musisz uzupełnić wszystkie pola {desc}'})
        Plan.objects.create(name=name, description=desc)
        my_id = Plan.objects.latest('pk').id
        return redirect(f"/plan/{my_id}/")


class AddRecipeToPlan(View):
    def get(self, request):
        return HttpResponse("Tu będzie dodawanie przepisu do planu")


def recipe(request):
    if Recipe.objects.all().count() > 0:
        recipes_list = Recipe.objects.all().order_by('-votes', 'created')
        paginator = Paginator(recipes_list, 50)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'jedzonko/app-recipes.html', {'page_obj': page_obj})
    else:
        return render(request, 'jedzonko/app-recipes.html', {'lackOfRecipes': "Chwilowo brak przepisów :("})


class PlanDetails(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        days = DayName.objects.filter(recipeplan__plan_id=id).distinct()
        meals = RecipePlan.objects.all()
        recipe_plan = RecipePlan.objects.filter(plan_id=id)
        context = {'plan': plan, 'recipe_plan': recipe_plan, 'days': days, 'meals': meals}
        return render(request, 'jedzonko/app-details-schedules.html', context)
