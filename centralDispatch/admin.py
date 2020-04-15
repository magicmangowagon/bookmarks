from django.contrib import admin
from .models import SolutionRouter, AssignmentKeeper, SomethingHappened


@admin.register(SolutionRouter)
class SolutionRouterAdmin(admin.ModelAdmin):
    fields = ['solutionInstance', 'routerChoices', 'name', ]


@admin.register(AssignmentKeeper)
class AssignmentKeepAdmin(admin.ModelAdmin):
    fields = ['userSolution', 'coach', 'evaluator', ]


@admin.register(SomethingHappened)
class SomethingHappenedAdmin(admin.ModelAdmin):
    fields = ['userSolution', 'archivedName', 'time']

