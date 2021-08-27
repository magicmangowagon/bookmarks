from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import LearningObjective, Rubric, Criterion, Competency, Challenge, UserSolution, RubricLine, CriteriaLine, \
    CompetencyProgress, ChallengeAddendum, LearningExperience, LearningExpoResponses, Evaluated, SolutionInstance, \
    MegaChallenge, CoachReview, ChallengeSolutionJunction, ChallengeResources, ChallengeResourcesFile, TfJSolution, \
    TfJEval, GeneralSolution, TempUserSolution, TempTfJSolution


class CriteriaInline(admin.TabularInline):
    model = Criterion
    fields = ['name', ]


class LearningObjsInline(admin.TabularInline):
    model = LearningObjective

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(LearningObjsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return field


class CompetencyInline(admin.TabularInline):
    model = Competency


class UserSolutionInline(admin.TabularInline):
    model = UserSolution.evaluated.through


class RubricLineInline(admin.TabularInline):
    model = RubricLine


class ChallengeOrderSort(SortableInlineAdminMixin, admin.TabularInline):
    model = Challenge
    fields = ('name', )
    extra = 0


class LearningExpoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = LearningExperience
    exclude = ['learningObjectives', 'description', 'tags']
    extra = 0


class ChallengeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Challenge
    # exclude = ['description']
    fields = ['name']
    extra = 0


class SolutionInstanceInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SolutionInstance
    extra = 0
    exclude = ['']


class ChallengeResourceFileInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ChallengeResourcesFile
    extra = 0


@admin.register(GeneralSolution)
class GeneralSolutionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'creator', 'solutionInstance', 'creationDate']
    pass


@admin.register(TempUserSolution)
class TempUserSolutionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'solutionInstance', 'customized']
    pass


@admin.register(TempTfJSolution)
class TempUserSolutionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'solutionInstance', 'creator']
    pass


@admin.register(UserSolution)
class UserSolution(admin.ModelAdmin):
    list_display = ['pk', 'userOwner', 'challengeName', 'solutionInstance', 'customized']
    pass


@admin.register(TfJSolution)
class TfJSolutionAdmin(admin.ModelAdmin):
    list_display = ('solutionInstance', 'solution', 'user', 'coachLO', 'tcLO')
    # filter_horizontal = ('learningObjectives',)


@admin.register(TfJEval)
class TfJEvalAdmin(admin.ModelAdmin):
    list_display = ('learningObjective', 'userSolution')


@admin.register(Evaluated)
class Evaluated(admin.ModelAdmin):
    list_display = ['whoEvaluated', 'date']
    inlines = [
        UserSolutionInline,
    ]


@admin.register(RubricLine)
class RubricLine(admin.ModelAdmin):
    list_display = ['pk', 'student', 'learningObjective']
    list_filter = ['student', 'learningObjective']


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
    list_display = ['name', 'display']
    filter_horizontal = ('learningObjs', 'solutions')
    inlines = [
        LearningExpoInline,
    ]


@admin.register(MegaChallenge)
class MegaChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'overRide', ]
    exclude = ['my_order']
    filter_horizontal = ['solutions', ]
    inlines = [
        ChallengeInline,
    ]


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
    list_display = ['evaluator', 'challenge', 'userSolution']


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
    list_display = ['release', 'comment', 'userSolution']


@admin.register(ChallengeResources)
class ChallengeResourcesAdmin(admin.ModelAdmin):
    list_display = ('name', 'challenge', 'megaChallenge',)
    inlines = [ChallengeResourceFileInline, ]
    filter_horizontal = ['learningExperience']


@admin.register(ChallengeResourcesFile)
class ChallengeResourcesFileAdmin(admin.ModelAdmin):
    list_display = ('challengeResources', 'file', )


