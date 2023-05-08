from django.contrib import admin
from jedzonko.models import *

# Register your models here.

admin.site.register(Recipe)
admin.site.register(Plan)
admin.site.register(DayName)
admin.site.register(RecipePlan)

