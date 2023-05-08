from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        return render(request, "jedzonko/index.html")


class Dashboard(View):
    def get(self, request):
        return render(request, "jedzonko/dashboard.html")


def recipe(request):
    return render(request, 'jedzonko/app-recipes.html')
