from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import LearningObjective, Rubric, Criterion, Competency, Challenge, UserSolution, RubricLine, CriteriaLine, \
    CompetencyProgress, ChallengeAddendum, LearningExperience, LearningExpoResponses, Evaluated, SolutionInstance, \
    MegaChallenge, CoachReview


class CriteriaInline(admin.TabularInline):
    model = Criterion


class LearningObjsInline(admin.TabularInline):
    model = LearningObjective

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(LearningObjsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return field


class CompetencyInline(admin.TabularInline):
    model = Competency


class UserSolutionInline(admin.TabularInline):
    model = UserSolution.evaluated.through


@admin.register(UserSolution)
class UserSolution(admin.ModelAdmin):
    list_display = ['pk', 'userOwner', 'challengeName', 'customized']
    pass


@admin.register(Evaluated)
class Evaluated(admin.ModelAdmin):
    list_display = ['whoEvaluated', 'date']
    inlines = [
        UserSolutionInline,
    ]


@admin.register(RubricLine)
class RubricLine(admin.ModelAdmin):
    list_display = ['pk', 'student', 'learningObjective']


@admin.register(CriteriaLine)
class CriteriaLine(admin.ModelAdmin):
    list_display = ['achievement', 'pk', 'userSolution']


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    # list_display = ['fullname', 'compNumber', 'loNumber', 'name']
    inlines = [
        CriteriaInline,
    ]

    def get_queryset(self, request):
        queryset = LearningObjective.objects.all().order_by('compGroup', 'compNumber', 'loNumber')
        return queryset


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ['compGroup', 'compNumber', 'name', 'description']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('learningObjs', 'solutions')


@admin.register(MegaChallenge)
class MegaChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'overRide']
    filter_horizontal = ['solutions', ]


@admin.register(SolutionInstance)
class SolutionInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']
    filter_horizontal = ['learningObjectives']


@admin.register(LearningExperience)
class LearningExpAdmin(admin.ModelAdmin):
    list_display = ['name', 'challenge']
    filter_horizontal = ('learningObjectives',)


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ['evaluator', 'challenge']


@admin.register(Criterion)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CompetencyProgress)
class CompProgressAdmin(admin.ModelAdmin):
    list_display = ['competency', 'student', 'attempted', 'complete']


@admin.register(ChallengeAddendum)
class ChallengeAddendumAdmin(admin.ModelAdmin):
    list_display = ['name', 'note', 'parentChallenge', 'userSolution', 'group']
    filter_horizontal = ('learningObjs',)


@admin.register(LearningExpoResponses)
class LearningExpoResponsesAdmin(admin.ModelAdmin):
    list_display = ['learningExperience', 'user']


@admin.register(CoachReview)
class CoachReviewAdmin(admin.ModelAdmin):
    list_display = ['rubricLine', 'release', 'comment']
