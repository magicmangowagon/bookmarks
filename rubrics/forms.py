from django import forms
from .models import LearningObjective, Challenge, UserSolution
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
        fields = ('file', )
