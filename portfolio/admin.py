from django.contrib import admin
from .models import Portfolio, UserPortfolio, TempUserPortfolio


# Register your models here.
@admin.register(Portfolio)
class SolutionInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']
    filter_horizontal = ['learningObjectives']


@admin.register(UserPortfolio)
class UserPortfolio(admin.ModelAdmin):
    list_display = ['pk', 'name', 'creation_date']
    filter_horizontal = ['team']


@admin.register(TempUserPortfolio)
class TempUserPortfolio(admin.ModelAdmin):
    list_display = ['pk', 'userOwner', 'challengeName', 'solutionInstance', 'customized']
    filter_horizontal = ['team', 'evaluated']
