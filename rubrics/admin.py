from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import LearningObjective, Rubric, Criterion, Competency, Challenge, UserSolution, RubricLine


class CriteriaInline(admin.TabularInline):
    model = Criterion


class LearningObjsInline(admin.TabularInline):
    model = LearningObjective
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(LearningObjsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return field


class CompetencyInline(admin.TabularInline):
    model = Competency


@admin.register(UserSolution)
class UserSolution(admin.ModelAdmin):
    list_display = ['userOwner', 'challengeName']


@admin.register(RubricLine)
class RubricLine(admin.ModelAdmin):
    list_display = ['student', 'learningObjective']


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    # list_display = ['fullname', 'compNumber', 'loNumber', 'name']
    inlines = [
        CriteriaInline,
    ]


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ['compGroup', 'compNumber', 'name', 'description']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('learningObjs',)


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ['evaluator', 'challenge']


@admin.register(Criterion)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name']
