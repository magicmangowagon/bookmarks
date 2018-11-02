from django import forms
from .models import LearningObjective


class RubricForm(forms.Form):
    learningObj = forms.ModelChoiceField(queryset=LearningObjective.objects.all().order_by('name'))
