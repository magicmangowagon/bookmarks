from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import LearningObjective, Rubric, Criterion, Competency, Challenge, UserSolution, RubricLine, UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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
    list_display = ['name', 'description']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Rubric)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Criterion)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name']
