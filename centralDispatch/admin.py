from django.contrib import admin
from .models import SolutionRouter, AssignmentKeeper, SomethingHappened, SolutionStatus, ChallengeStatus


@admin.register(SolutionRouter)
class SolutionRouterAdmin(admin.ModelAdmin):
    fields = ['solutionInstance', 'routerChoices', 'name', ]


@admin.register(AssignmentKeeper)
class AssignmentKeepAdmin(admin.ModelAdmin):
    fields = ['userSolution', 'coach', 'evaluator']


@admin.register(SomethingHappened)
class SomethingHappenedAdmin(admin.ModelAdmin):
    fields = ['userSolution', 'archivedName', 'time', 'created', 'modified']
    list_display = ['userSolution', 'created']
    readonly_fields = ['created', 'modified']


@admin.register(ChallengeStatus)
class ChallengeStatusAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'user', 'challengeAccepted']
    filter_horizontal = ['solutionStatusByInstance']


@admin.register(SolutionStatus)
class SolutionStatusAdmin(admin.ModelAdmin):
    list_display = ['solutionInstance', 'userSolution']
    fields = ['solutionInstance', 'userSolution', 'solutionSubmitted', 'solutionEvaluated', 'solutionCoachReviewed',
              'solutionRejected', 'returnTo', 'solutionCompleted']

