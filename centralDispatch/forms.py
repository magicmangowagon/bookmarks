from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ModelForm
from rubrics.models import Challenge, UserSolution, Rubric, RubricLine, CriteriaLine, \
    ChallengeAddendum, LearningExperience, LearningExpoResponses, CoachReview
from .models import SolutionRouter, AssignmentKeeper, ChallengeStatus
from django.contrib.auth.models import User

# create form for router, then a form for manual assignment. Going to have to dig into AJAX to make this work
# smoothly for Hannah.


class SolutionRouterForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(SolutionRouterForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'name': forms.HiddenInput}


class AssignmentKeeperForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(AssignmentKeeperForm, self).__init__(*args, **kwargs)


class SolutionRouterFormB(forms.ModelForm):
    class Meta:
        model = SolutionRouter
        fields = ['coach', 'challenge', 'solutionInstance', 'automate', 'routerChoices']


class ChallengeStatusForm(forms.ModelForm):
    class Meta:
        model = ChallengeStatus
        fields = ['challengeAccepted', 'user', 'challenge']


ChallengeStatusFormset = modelformset_factory(ChallengeStatus, extra=0, fields=('user', 'challenge'))


SolutionRouterFormset = modelformset_factory(SolutionRouter, extra=0, formset=SolutionRouterForm,
                                             fields=('coach', 'challenge', 'solutionInstance', 'automate', 'routerChoices'),
                                             widgets={'name': forms.HiddenInput()})

NewSolutionFormset = modelformset_factory(AssignmentKeeper, extra=0, formset=AssignmentKeeperForm, fields=('evaluator', 'coach', ),)
