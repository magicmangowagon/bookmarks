from django import forms
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
        fields = ('file', 'challengeName', 'userOwner')
        widgets = {'challengeName': forms.HiddenInput(), 'userOwner': forms.HiddenInput}


class RubricLineForm(forms.Form):
    class Meta:
        model = RubricLine
        fields = ('evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'readiness')
