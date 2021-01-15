from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ModelForm
from rubrics.models import Challenge, UserSolution, LearningObjective
from .models import UserPortfolio, Portfolio
from django.contrib.auth.models import User


class UserPortfolioForm(forms.ModelForm):
    chosenLearningObjs = forms.ModelMultipleChoiceField(queryset=LearningObjective.objects.all())

    class Meta:
        model = UserPortfolio
        fields = ['creator', 'chosenLearningObjs', 'portfolio', 'link', 'proudDetail', 'hardDetail']
        widgets = {'creator': forms.HiddenInput, 'portfolio': forms.HiddenInput}

    def __init__(self, portfolio, *args, **kwargs):
        super(UserPortfolioForm, self).__init__(*args, **kwargs)
        self.fields['chosenLearningObjs'].queryset = portfolio.learningObjectives.all()
