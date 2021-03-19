# builtins
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.detail import SingleObjectMixin
# custom
from .models import LoEvaluation, GeneralEvaluation, CriteriaEvaluation
from rubrics.models import UserSolution
from .forms import GeneralEvaluationInlineFormset


# Create your views here.
class EvaluationView(FormView):
    template_name = 'evaluation/evaluation.html'
    model = UserSolution
    form_class = GeneralEvaluationInlineFormset

    def get_context_data(self, **kwargs):
        context = super(EvaluationView, self).get_context_data(**kwargs)
        context['form'] = GeneralEvaluationInlineFormset
        return context
