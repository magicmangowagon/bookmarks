from django import forms
from django.forms import modelformset_factory, ModelForm, BaseModelFormSet
from .models import LearningObjective, Challenge, UserSolution, Rubric, RubricLine
from django.views.generic import DetailView


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
        fields = ('file', 'solution', 'challengeName', 'userOwner')
        widgets = {'challengeName': forms.HiddenInput(), 'userOwner': forms.HiddenInput}


class RubricLineForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricLineForm, self).__init__(*args, **kwargs)


class RubricForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricForm, self).__init__(*args, **kwargs)


RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, fields=('evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel', 'student',
                  'learningObjective', ))

RubricFormSet = modelformset_factory(Rubric, formset=RubricForm, fields=('generalFeedback', 'userSolution', 'challengeCompletionLevel', 'evaluator', 'challenge'))
