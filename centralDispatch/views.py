from django.shortcuts import render
from rubrics.models import UserSolution, Challenge, Evaluated, SolutionInstance
from account.models import Profile
from django.contrib.auth.models import User
from .models import SolutionRouter, ManualAssignmentKeeper
from django.views.generic import ListView, DetailView, FormView
from .forms import SolutionRouterForm
from django.forms import BaseModelFormSet, modelformset_factory


# Create your views here.
class NewSolutionDispatch(ListView):
    context_object_name = 'newSolutions'
    queryset = UserSolution.objects.all().filter(evaluated__isnull=True)
    template_name = 'centralDispatch/newSolutionDispatch.html'

    def get_context_data(self, **kwargs):
        context = super(NewSolutionDispatch, self).get_context_data()
        challenges = Challenge.objects.all().filter(display=True).order_by('challengeGroupChoices')
        solutionInstances = SolutionInstance.objects.all().filter(challenge_that_owns_me__in=challenges)

        SolutionRouterFormset = modelformset_factory(SolutionRouter, extra=0,
                                                     formset=SolutionRouterForm, fields=('profile',
                                                                                         'challenge',
                                                                                         'solutionInstance',
                                                                                         'automate',
                                                                                         'routerChoices'), )
        solutionRouterFormset = SolutionRouterFormset(prefix='routerFormset', queryset=SolutionRouter.objects.all().filter(
            solutionInstance__challenge_that_owns_me__in=challenges).order_by('challenge__challengeGroupChoices'))

        context['formset'] = solutionRouterFormset
        context['challenges'] = challenges
        context['solutionInstances'] = solutionInstances
        return context
