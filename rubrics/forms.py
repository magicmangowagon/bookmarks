from django import forms
from django.forms import modelformset_factory, ModelForm, BaseModelFormSet, inlineformset_factory
from .models import LearningObjective, Challenge, UserSolution, Rubric, RubricLine, CriteriaLine, Criterion
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
        fields = ('solution', 'challengeName', 'userOwner')
        widgets = {'challengeName': forms.HiddenInput(), 'userOwner': forms.HiddenInput}


class RubricLineForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricLineForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'student': forms.HiddenInput(), }


class RubricForm(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RubricForm, self).__init__(*args, **kwargs)


class CriteriaForm(ModelForm):
    class Meta:
        model = CriteriaLine
        fields = ('criteria', 'achievement', 'userSolution', )


CriterionFormSet = inlineformset_factory(Criterion, CriteriaLine, form=CriteriaForm)


RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, fields=('evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel', 'student',
                  'learningObjective', ))

RubricFormSet = modelformset_factory(Rubric, formset=RubricForm, fields=('generalFeedback', 'userSolution', 'challengeCompletionLevel', 'evaluator', 'challenge'))
