from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import modelformset_factory, ModelForm, BaseModelFormSet, inlineformset_factory
from .models import LearningObjective, Challenge, UserSolution, Rubric, RubricLine, CriteriaLine, Criterion, ChallengeAddendum, LearningExperience, LearningExpoResponses
from django.views.generic import DetailView
from django.contrib.auth.models import User
from account.models import Profile


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('name', 'description', 'learningObjs')


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


class UserFileForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(UserFileForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'challengeName': forms.HiddenInput(), 'userOwner': forms.HiddenInput}


class LearningExperienceForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(LearningExperienceForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {''}


class LearningExpoFeedbackForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(LearningExpoFeedbackForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'user': forms.HiddenInput()}


UserFileFormset = modelformset_factory(UserSolution, formset=UserFileForm, fields=('userOwner', 'challengeName', 'solution',
    'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective',
   'helpfulLearningExp', 'notHelpfulLearningExp', 'changeLearningExp', 'notIncludedLearningExp'),
                                       widgets={'challengeName': forms.HiddenInput(), 'userOwner': forms.HiddenInput})


CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, fields=('achievement', 'criteria',
                                                                                    'userSolution'))


RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, fields=('ignore', 'evidencePresent',
                 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel', 'student', 'learningObjective',
                                                                                     'needsLaterAttention', ))

RubricAddendumFormset = modelformset_factory(ChallengeAddendum, formset=RubricAddendumForm, fields=('name', 'note',
                                                'parentChallenge', 'learningObjs', 'tags', 'group', 'userSolution'))


RubricFormSet = modelformset_factory(Rubric, formset=RubricForm, fields=('generalFeedback', 'challenge',
                                                 'challengeCompletionLevel', 'evaluator', 'userSolution'))


LearningExperienceFormset = modelformset_factory(LearningExperience, formset=LearningExperienceForm, fields=('name',
                 'challenge', 'learningObjectives', 'description', 'tags'))


LearningExpoFeedbackFormset = modelformset_factory(LearningExpoResponses, formset=LearningExpoFeedbackForm, fields=(
    'learningExperienceResponse', 'learningExperience', 'user'), widgets={'user': forms.HiddenInput()})
