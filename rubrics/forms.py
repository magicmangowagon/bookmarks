from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import modelformset_factory, ModelForm, BaseModelFormSet, inlineformset_factory
from .models import LearningObjective, Challenge, UserSolution, Rubric, RubricLine, CriteriaLine, Criterion, ChallengeAddendum, FeedbackFrame
from django.views.generic import DetailView
from django.contrib.auth.models import User
from account.models import Profile


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('name', 'description', 'learningObjs')


class ChallengeDisplay(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserFileForm()
        return context


class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserSolution
        fields = ('solution', 'challengeName', 'userOwner', 'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective')
        widgets = {'challengeName': forms.HiddenInput(), 'userOwner': forms.HiddenInput}


class CurrentStudentToView(forms.Form):
    chooseUser = forms.ModelChoiceField(queryset=User.objects.all().filter(profile__role=1), initial=0, label='Choose User')


class FramingFeedbackForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(FramingFeedbackForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'userSolution', forms.HiddenInput()}


class RubricLineForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricLineForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'student': forms.HiddenInput()}


class RubricAddendumForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricAddendumForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'userSolution': forms.HiddenInput()}


class RubricForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricForm, self).__init__(*args, **kwargs)


class CriteriaForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(CriteriaForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'criteria': forms.HiddenInput(), }


FramingFeedbackFormSet = modelformset_factory(FeedbackFrame, formset=FramingFeedbackForm, fields=('user', 'challenge',
    'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective'))


CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, fields=('achievement', 'criteria', 'userSolution'))


RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, fields=('ignore', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel', 'student',
                  'learningObjective', 'needsLaterAttention', ))

RubricAddendumFormset = modelformset_factory(ChallengeAddendum, formset=RubricAddendumForm, fields=('name', 'note', 'parentChallenge', 'learningObjs', 'group', 'userSolution'))


RubricFormSet = modelformset_factory(Rubric, formset=RubricForm, fields=('generalFeedback', 'userSolution', 'challengeCompletionLevel', 'evaluator', 'challenge'))
