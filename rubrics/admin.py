from django.contrib import admin
from .models import LearningObjective, Rubric, Criterion


class CriteriaInline(admin.TabularInline):
    model = Criterion


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    inlines = [
        CriteriaInline,
    ]


@admin.register(Rubric)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Criterion)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name']
