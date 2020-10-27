from django_filters import FilterSet, filters
from .models import SolutionStatus, ChallengeStatus
from rubrics.models import Evaluated, SolutionInstance
from rubrics.models import User
from django.forms import forms


class SolutionTrackerFilter(FilterSet):
    # userOwner = filters.ModelChoiceFilter(queryset=User.objects.all().filter(profile__role=1))
    completedChoices = (
        (None, 'All'),
        (True, 'Yes'),
        (False, 'No')
    )

    def get_full_names():
        full_names = ()
        users = User.objects.filter(profile__role=1).filter(is_active=True).order_by('last_name')
        for user in users:
            full_names += (user.id, str(user.last_name + ', ' + str(user.first_name))),
        return full_names

    # evaluators = Evaluated.objects.all().order_by('whoEvaluated').distinct('whoEvaluated')
    tc = filters.ChoiceFilter(field_name='userSolution__userOwner', label='Teacher Candidate',
                                   choices=get_full_names(), empty_label='All')
    solutionCompleted = filters.ChoiceFilter(field_name='solutionCompleted', choices=completedChoices,
                                             lookup_expr='exact', empty_label=None, label='Completed')
    evaluator = filters.ModelChoiceFilter(field_name='userSolution__evaluated__whoEvaluated',
                                          queryset=User.objects.filter(profile__role__gte=2),
                                          label='Evaluator', empty_label='All')

    solutionInstance = filters.ModelChoiceFilter(field_name='userSolution__solutionInstance', empty_label='All',
                                                 queryset=SolutionInstance.objects.all().order_by(
                                                     'challenge_that_owns_me__challengeGroupChoices'),
                                                 label='Solution Instance')

    class Meta:
        model = SolutionStatus
        fields = {'tc', 'solutionInstance',
                  'evaluator', 'solutionCompleted'}
