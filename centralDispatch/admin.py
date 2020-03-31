from django.contrib import admin
from .models import SolutionRouter, AssignmentKeeper


@admin.register(SolutionRouter)
class SolutionRouterAdmin(admin.ModelAdmin):
    fields = ['solutionInstance', 'routerChoices', 'name', ]


@admin.register(AssignmentKeeper)
class AssignmentKeepAdmin(admin.ModelAdmin):
    fields = ['userSolution', 'coach', 'evaluator', ]

