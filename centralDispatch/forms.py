from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ModelForm
from rubrics.models import Challenge, UserSolution, Rubric, RubricLine, CriteriaLine, \
    ChallengeAddendum, LearningExperience, LearningExpoResponses, CoachReview
from .models import SolutionRouter, AssignmentKeeper, ChallengeStatus, SolutionStatus, StudioExpoChoice
from info.models import BaseInfo
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


class SolutionStatusForm(BaseModelFormSet):
    class Meta:
        model = SolutionStatus
        fields = ['solutionRejected', 'returnTo', 'solutionCompleted']
        widgets = {'solutionRejected': forms.HiddenInput, 'solutionCompleted': forms.HiddenInput}


class UserWorkToView(forms.Form):
    chooseUser = forms.ModelChoiceField(queryset=User.objects.all().filter(profile__role=1).filter(
        is_active=True).order_by('last_name'), initial=0, required=True, label='Choose User',)
    fields = ['chooseUser']


class AllUsersForm(forms.Form):
    chooseUser = forms.ModelChoiceField(queryset=User.objects.all().filter(is_active=True))
    fields = ['chooseUser']


class StudioExpoChoiceForm(forms.ModelForm):
    learningExpoChoice = forms.ModelChoiceField(queryset=LearningExperience.objects.all(), empty_label=None)

    class Meta:
        model = StudioExpoChoice
        fields = ['user', 'learningExpoChoice', 'session']
        widgets = {'user': forms.HiddenInput(), 'session': forms.HiddenInput(), }

    def __init__(self, baseInfo, *args, **kwargs):
        super(StudioExpoChoiceForm, self).__init__(*args, **kwargs)
        self.fields['learningExpoChoice'].widget = forms.RadioSelect()
        self.fields['learningExpoChoice'].queryset = baseInfo.learningExpos.all()


ChallengeStatusFormset = modelformset_factory(ChallengeStatus, extra=0, fields=('user', 'challenge', 'challengeAccepted'))

solutionStatusFormset = modelformset_factory(SolutionStatus, extra=0, formset=SolutionStatusForm, fields=('returnTo',))

SolutionRouterFormset = modelformset_factory(SolutionRouter, extra=0, formset=SolutionRouterForm,
                                             fields=('coach', 'challenge', 'solutionInstance', 'automate', 'routerChoices'),
                                             widgets={'name': forms.HiddenInput()})

NewSolutionFormset = modelformset_factory(AssignmentKeeper, extra=0, formset=AssignmentKeeperForm, fields=('evaluator', 'coach', ),)
