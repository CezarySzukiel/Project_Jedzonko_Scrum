"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko import views as jedzonko_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jedzonko_views.IndexView.as_view()),
    path('main/', jedzonko_views.Dashboard.as_view()),

    path('recipe/<int:id>/', jedzonko_views.RecipeView.as_view()),
    # path('recipe/list/', jedzonko_views.RecipeList.as_view()),
    path('recipe/add/', jedzonko_views.AddRecipe.as_view(), name='add_recipe'),
    path('recipe/modify/<int:id>/', jedzonko_views.ModifyRecipe.as_view()),
    path('plan/list/', jedzonko_views.PlanList.as_view()),
    path('plan/add/', jedzonko_views.AddPlan.as_view()),
    path('plan/add-recipe/', jedzonko_views.AddRecipeToPlan.as_view()),
    path('recipe/list/', jedzonko_views.recipe, name='recipe'),
    path('plan/<int:id>/', jedzonko_views.PlanDetails.as_view(), name='plan_details'),
]
