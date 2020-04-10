from .models import Rubric, RubricLine, UserSolution, CoachReview
from account.models import Profile
from django.contrib.auth.models import User, Group
import django_filters
from django_filters import filters


class EvalFilter(django_filters.FilterSet):

    userOwner = filters.ModelChoiceFilter(queryset=User.objects.all().filter(profile__role=1))

    class Meta:
        model = UserSolution
        # evaluators = User.objects.all().filter(profile__role=2 or 3 or 4)
        fields = {'userOwner', 'challengeName', 'solutionInstance', 'coachReview__release', 'evaluated__whoEvaluated'}

