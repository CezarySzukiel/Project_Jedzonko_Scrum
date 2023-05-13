from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
import random

from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        page = [page_slug.slug for page_slug in Page.objects.all()]
        if Recipe.objects.all().count() > 0:
            recipes = []
            for my_recipe in Recipe.objects.all():
                recipes.append([my_recipe.name, my_recipe.description])
            random.shuffle(recipes)

            names = [i[0] for i in recipes[:3]]
            descriptions = [i[1] for i in recipes[:3]]
            return render(request, "jedzonko/index.html", {'names': names,
                                                           'descriptions': descriptions,
                                                           'Recipes': "true",
                                                           'pages': page})

        else:
            return render(request, "jedzonko/index.html", {'lackOfRecipes': "Chwilowo brak przepisów :(",
                                                           'pages': page})


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


class About(View):
    def get(self, request):
        page = [page_slug.slug for page_slug in Page.objects.all()]
        return render(request, 'jedzonko/about.html', {'page': page})


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

    def post(self, request, id_):
        my_id = int(request.POST.get("my_id"))
        recipe_ = Recipe.objects.get(pk=my_id)

        if 'like' in request.POST:
            recipe_.votes = recipe_.votes + 1
            recipe_.save()

        if 'dislike' in request.POST:
            recipe_.votes = recipe_.votes - 1
            recipe_.save()

        return redirect(f'/recipe/{my_id}/')


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
    def get(self, request, id_):
        try:
            recipe_ = Recipe.objects.get(pk=id_)
        except ObjectDoesNotExist:
            raise Http404
        preparation = [i for i in recipe_.preparation_method.split("\n") if i and i != '\r']
        ingredients = [i for i in recipe_.ingredients.split("\n") if i and i != '\r']
        return render(request, 'jedzonko/app-edit-recipe.html', {
            'recipe': recipe_,
            'preparation': preparation,
            'ingredients': ingredients,
        })

    def post(self, request, id_):
        recipe_ = Recipe.objects.get(pk=id_)
        name = request.POST.get('name')
        description = request.POST.get('description')
        time = request.POST.get('time')

        preparation = request.POST.get('preparation')
        ingredients = request.POST.get('ingredients')

        if not (name and description and time and preparation and ingredients):
            preparation = [i for i in recipe_.preparation_method.split("\n") if i and i != '\r']
            ingredients = [i for i in recipe_.ingredients.split("\n") if i and i != '\r']
            return render(request, 'jedzonko/app-edit-recipe.html',
                          {'message': 'Musisz uzupełnić wszystkie pola',
                           'recipe': recipe_,
                           'preparation': preparation,
                           'ingredients': ingredients})

        if int(time) < 1:
            preparation = [i for i in recipe_.preparation_method.split("\n") if i and i != '\r']
            ingredients = [i for i in recipe_.ingredients.split("\n") if i and i != '\r']
            return render(request, 'jedzonko/app-edit-recipe.html',
                          {'message': 'Minimalny czas to 1 minuta',
                           'recipe': recipe_,
                           'preparation': preparation,
                           'ingredients': ingredients})

        recipe_.name = name
        recipe_.description = description
        recipe_.preparation_time = time
        recipe_.ingredients = ingredients
        recipe_.preparation_method = preparation
        recipe_.save()

        return redirect('/recipe/list/')


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

    def post(self, request):
        plan_id = request.POST.get('id')
        Plan.objects.get(pk=plan_id).delete()
        return redirect('/plan/list/')


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
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        plan_id = request.GET.get('plan_id')
        recipe_id = request.GET.get('recipe_id')
        return render(request, 'jedzonko/app-schedules-meal-recipe.html',
                      {'plans': plans,
                       'recipes': recipes,
                       'days': days,
                       'plan_id': convert_to_int(plan_id),
                       'recipe_id': convert_to_int(recipe_id)})

    def post(self, request):
        plan = request.POST.get('plan')
        meal_name = request.POST.get('name')
        meal_number = request.POST.get('number')
        recipe_id = request.POST.get('recipe')
        day = request.POST.get('day')

        if not (meal_name or meal_number):
            return HttpResponse('Pola nie mogą być puste')

        try:
            meal_number = int(meal_number)
        except ValueError:
            return HttpResponse('Numer musi być liczbą')

        RecipePlan.objects.create(meal_name=meal_name, order=meal_number, day_name_id=day,
                                  plan_id=plan, recipe_id=recipe_id)

        return redirect(f'/plan/{plan}')


class RecipeViews(View):
    def get(self, request):
        if Recipe.objects.all().count() > 0:
            error = None
            recipes_list = Recipe.objects.all().order_by('-votes', 'created')

            paginator = Paginator(recipes_list, 50)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(request, 'jedzonko/app-recipes.html', {'page_obj': page_obj, 'error': error})
        else:
            return render(request, 'jedzonko/app-recipes.html', {'lackOfRecipes': "Chwilowo brak przepisów :("})

    def post(self, request):
        recipe_id = request.POST.get('id')
        if Recipe.objects.all().count() > 0:
            error = None
            recipes_list = Recipe.objects.all().order_by('-votes', 'created')

            if "search" in request.POST:
                searchQuery = request.POST.get("searchText")
                recipes_list = Recipe.objects.all().filter(name__icontains=searchQuery).order_by('-votes', 'created')
                if recipes_list.count() < 1:
                    error = "Nie ma przepisów o takiej nazwie"
                    recipes_list = Recipe.objects.all().order_by('-votes', 'created')

                paginator = Paginator(recipes_list, 50)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

                return render(request, 'jedzonko/app-recipes.html', {'page_obj': page_obj, 'error': error})
        Recipe.objects.get(pk=recipe_id).delete()
        return redirect('/recipe/list/')


class PlanDetails(View):
    def get(self, request, id_):
        plan = Plan.objects.get(pk=id_)
        days = DayName.objects.filter(recipeplan__plan_id=id_).distinct()
        meals = RecipePlan.objects.all()
        recipe_plan = RecipePlan.objects.filter(plan_id=id_)
        plan_id = request.GET.get('plan_id')
        context = {'plan': plan, 'recipe_plan': recipe_plan, 'days': days, 'meals': meals,
                   'plan_id': convert_to_int(plan_id)}
        return render(request, 'jedzonko/app-details-schedules.html', context)

    def post(self, request, id_):
        meal_id = request.POST.get('id')
        RecipePlan.objects.get(pk=meal_id).delete()
        return redirect(f'/plan/{id_}')


class Contact(View):
    def get(self, request):
        page = [page_slug.slug for page_slug in Page.objects.all()]
        return render(request, 'jedzonko/contact.html', {'page': page})


class EditPlan(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        print('przesłano metodą get')
        return render(request, 'jedzonko/app-edit-schedules.html', {'plan': plan})

    def post(self, request, plan_id):
        print('przesłano metodą post')
        plan = Plan.objects.get(pk=plan_id)
        name = request.POST.get('planName')
        desc = request.POST.get('planDescription')
        print('name i desc: ', name, desc)
        if not (name and desc):
            return HttpResponse('Pola nie mogą być puste')

        plan.name = name
        plan.description = desc
        plan.save()
        return redirect(f'/plan/{plan.id}')


def convert_to_int(value):
    if value:
        return int(value)
