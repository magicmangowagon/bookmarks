from django import forms
from django.forms import formset_factory, ModelForm
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


class RubricLineForm(ModelForm):
    class Meta:
        model = RubricLine
        fields = ('evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel')
        widgets = {'solutionOwner': forms.HiddenInput(), 'learningObjective': forms.HiddenInput()}


class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ('description',)
        widgets = {'challenge': forms.HiddenInput, }


RubricLineFormset = formset_factory(RubricLineForm)
