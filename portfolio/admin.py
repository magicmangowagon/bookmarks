from django.contrib import admin
from .models import Portfolio, UserPortfolio


# Register your models here.
@admin.register(Portfolio)
class SolutionInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']
    filter_horizontal = ['learningObjectives']


@admin.register(UserPortfolio)
class UserPortfolio(admin.ModelAdmin):
    list_display = ['pk', 'name', 'creation_date']
    filter_horizontal = ['team']
