from django.contrib import admin
from .models import LearningObjective


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
