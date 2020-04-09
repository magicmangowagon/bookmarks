from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rubrics.models import UserSolution, Challenge, Evaluated, SolutionInstance, MegaChallenge
from account.models import Profile
from django.contrib.auth.models import User
from .models import SolutionRouter, AssignmentKeeper
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin, UpdateView
from .forms import SolutionRouterForm, AssignmentKeeperForm, SolutionRouterFormset, SolutionRouterFormB, NewSolutionFormset
from django.forms import BaseModelFormSet, modelformset_factory
from django import forms
from django.http import HttpResponseRedirect
from .functions import submissionAlert, evaluatorAssigned


# Create your views here.
class SolutionDispatch(FormView):
    model = SolutionRouter
    form_class = SolutionRouterFormB
    formset_class = SolutionRouterFormset
    template_name = 'centralDispatch/SolutionDispatch.html'
    success_url = reverse_lazy('central-dispatch')

    def get_context_data(self, **kwargs):
        context = super(SolutionDispatch, self).get_context_data(**kwargs)
        challenges = MegaChallenge.objects.all().filter(challenge__solutions__isnull=False).distinct().order_by('challengeGroupChoices')
        solutionInstances = SolutionInstance.objects.all().filter(challenge_that_owns_me__megaChallenge__in=challenges).distinct()

        SolutionRouterFormset = modelformset_factory(SolutionRouter, extra=0,
                                                     formset=SolutionRouterForm, fields=('name',
                                                                                         'coach',
                                                                                         'challenge',
                                                                                         'solutionInstance',
                                                                                         'automate',
                                                                                         'routerChoices'), widgets={'name': forms.HiddenInput})
        solutionRouterFormset = SolutionRouterFormset(prefix='routerFormset', queryset=SolutionRouter.objects.all().filter(
            solutionInstance__challenge_that_owns_me__megaChallenge__in=challenges).order_by('challenge__challengeGroupChoices'))

        context['solutionRouterFormset'] = solutionRouterFormset
        context['challenges'] = challenges
        context['solutionInstances'] = solutionInstances

        return context

    def post(self, request, *args, **kwargs):
        solutionRouterFormset = SolutionRouterFormset(request.POST, prefix='routerFormset')

        if solutionRouterFormset.is_valid():
            solutionRouterFormset.save()
            return self.form_valid(solutionRouterFormset)
        else:
            print(solutionRouterFormset.errors)
            return render(request, 'centralDispatch/SolutionDispatch.html', {"solutionRouterFormset": solutionRouterFormset})


class NewSolutionDispatch(FormView):
    template_name = 'centralDispatch/newSolutionDispatch.html'
    model = AssignmentKeeper
    form_class = NewSolutionFormset
    formset_class = NewSolutionFormset
    success_url = reverse_lazy('central-dispatch-new-solutions')

    def get_context_data(self, **kwargs):
        context = super(NewSolutionDispatch, self).get_context_data(**kwargs)

        newSubmissions = UserSolution.objects.filter(evaluated__isnull=True).filter(assignmentkeeper__evaluator__isnull=True).distinct()
        solutionInstances = SolutionInstance.objects.filter(usersolution__in=newSubmissions).order_by('usersolution__challengeName__challengeGroupChoices')
        NewSubmissionFormset = modelformset_factory(AssignmentKeeper, extra=0,
                                                    formset=AssignmentKeeperForm,
                                                    fields=('evaluator', 'coach', 'userSolution'))
        newSubmissionFormset = NewSubmissionFormset(prefix='newSolutions',
                                                    queryset=AssignmentKeeper.objects.filter(
                                                        userSolution__in=newSubmissions).order_by('userSolution__challengeName__challengeGroupChoices'))

        context['newSubmissionsFormset'] = newSubmissionFormset
        context['solutionInstances'] = solutionInstances
        return context

    def post(self, request, *args, **kwargs):
        newSolutionFormset = NewSolutionFormset(request.POST, prefix='newSolutions')
        newSubmissions = UserSolution.objects.filter(evaluated__isnull=True)
        # solutionInstances = SolutionRouter.objects.filter(usersolution__in=newSubmissions).order_by('usersolution__challengeName__challengeGroupChoices')
        asd = AssignmentKeeper.objects.filter(userSolution__in=newSubmissions).exclude(evaluator__isnull=True)
        if newSolutionFormset.is_valid():
            newSolutionFormset.save()
            for assignmentKeeper in asd:
                evaluatorAssigned(assignmentKeeper)
            return self.form_valid(newSolutionFormset)
        else:
            print(newSolutionFormset.errors)
            return render(request, 'centralDispatch/newSolutionDispatch.html', {"newSubmissionFormset": newSolutionFormset})


class AssignedSolutions(ListView):
    template_name = 'centralDispatch/assignedsolutions.html'
    queryset = UserSolution.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssignedSolutions, self).get_context_data()
        if self.request.user.profile.role == 1:
            tc = UserSolution.objects.all().filter(userOwner=self.request.user)
            context['solutionQueryset'] = tc
        elif self.request.user.profile.role == 2:
            evaluator = UserSolution.objects.all().filter(assignmentkeeper__evaluator=self.request.user.profile)
            context['solutionQueryset'] = evaluator
        elif self.request.user.profile.role == 3:
            coach = UserSolution.objects.all().filter(assignmentkeeper__coach=self.request.user.profile)
            context['solutionQueryset'] = coach
        elif self.request.user.profile.role == 4:
            everyone = UserSolution.objects.all()
            context['solutionQueryset'] = everyone

        return context
