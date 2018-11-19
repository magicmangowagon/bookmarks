from django import forms
from .models import LearningObjective, Challenge, UserSolution


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('name', 'description', 'learningObjs')


class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserSolution
        fields = ('file', )
