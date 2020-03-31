from django.shortcuts import render
from rubrics.models import UserSolution, Challenge, Evaluated, SolutionInstance, MegaChallenge
from account.models import Profile
from django.contrib.auth.models import User
from .models import SolutionRouter, AssignmentKeeper
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from .forms import SolutionRouterForm, ManualAssignmentKeeperForm
from django.forms import BaseModelFormSet, modelformset_factory


# Create your views here.
class SolutionDispatch(ListView):
    model = SolutionRouter
    template_name = 'centralDispatch/SolutionDispatch.html'

    def get_context_data(self, **kwargs):
        context = super(SolutionDispatch, self).get_context_data(**kwargs)
        challenges = MegaChallenge.objects.all().filter(challenge__solutions__isnull=False).distinct().order_by('challengeGroupChoices')
        solutionInstances = SolutionInstance.objects.all().filter(challenge_that_owns_me__megaChallenge__in=challenges).distinct()

        SolutionRouterFormset = modelformset_factory(SolutionRouter, extra=0,
                                                     formset=SolutionRouterForm, fields=('coach',
                                                                                         'challenge',
                                                                                         'solutionInstance',
                                                                                         'automate',
                                                                                         'routerChoices'), )
        solutionRouterFormset = SolutionRouterFormset(prefix='routerFormset', queryset=SolutionRouter.objects.all().filter(
            solutionInstance__challenge_that_owns_me__megaChallenge__in=challenges).order_by('challenge__challengeGroupChoices'))

        context['solutionRouterFormset'] = solutionRouterFormset
        context['challenges'] = challenges
        context['solutionInstances'] = solutionInstances

        if self.request.method == 'POST':
            form = solutionRouterFormset
            if form.is_valid():
                form.save()
                return render(self.request, self.template_name)

            else:
                return render(self.request, self.template_name, {'solutionRouterFormset': solutionRouterFormset})
        return context


class NewSolutionDispatch(ListView):
    template_name = 'centralDispatch/newSolutionDispatch.html'
    model = AssignmentKeeper

    def get_context_data(self, **kwargs):
        context = super(NewSolutionDispatch, self).get_context_data(**kwargs)

        newSubmissions = UserSolution.objects.filter(evaluated__isnull=True)
        NewSubmissionFormset = modelformset_factory(AssignmentKeeper, extra=0,
                                                    formset=ManualAssignmentKeeperForm,
                                                    fields=('evaluator', 'coach', 'userSolution'))
        newSubmissionFormset = NewSubmissionFormset(prefix='newSolutions',
                                                    queryset=AssignmentKeeper.objects.filter(
                                                        userSolution__in=newSubmissions).order_by('userSolution__challengeName__challengeGroupChoices'))

        context['newSubmissionsFormset'] = newSubmissionFormset
        return context
