from django.contrib import admin
from .models import LearningObjective, Rubric, Criterion, Competency, Challenge


class CriteriaInline(admin.TabularInline):
    model = Criterion


class LearningObjsInline(admin.TabularInline):
    model = LearningObjective

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(LearningObjsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return field


class CompetencyInline(admin.TabularInline):
    model = Competency


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    inlines = [
        CriteriaInline,
    ]


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Rubric)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Criterion)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name']
