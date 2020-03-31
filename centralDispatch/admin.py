from django.contrib import admin
from .models import SolutionRouter


@admin.register(SolutionRouter)
class SolutionRouterAdmin(admin.ModelAdmin):
    fields = ['challenge', 'coach', 'name',]
