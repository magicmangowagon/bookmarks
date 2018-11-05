from django import forms
from .models import LearningObjective, Challenge


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('name', 'description', 'learningObjs')
