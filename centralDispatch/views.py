from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rubrics.models import UserSolution, Challenge, Evaluated, SolutionInstance, MegaChallenge
from account.models import Profile
from django.contrib.auth.models import User
from .models import SolutionRouter, AssignmentKeeper, ChallengeStatus, SolutionStatus
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin, UpdateView
from .forms import SolutionRouterForm, AssignmentKeeperForm, SolutionRouterFormset, SolutionRouterFormB, NewSolutionFormset
from django.forms import BaseModelFormSet, modelformset_factory
from django import forms
from django.http import HttpResponseRedirect
from .functions import submissionAlert, evaluatorAssigned
from django_tables2 import SingleTableView, LazyPaginator, SingleTableMixin
from .tables import SolutionTable, ChallengeTable
from django_filters.views import FilterView
from .filters import SolutionTrackerFilter


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

        newSubmissions = UserSolution.objects.filter(evaluated__isnull=True).filter(assignmentkeeper__coach__isnull=True).filter(
            coachReview__isnull=True).filter(userOwner__is_active=True).distinct()
        solutionInstances = SolutionInstance.objects.filter(usersolution__in=newSubmissions).order_by('usersolution__challengeName__challengeGroupChoices')
        NewSubmissionFormset = modelformset_factory(AssignmentKeeper, extra=0,
                                                    formset=AssignmentKeeperForm,
                                                    fields=('evaluator', 'coach', 'userSolution'))
        newSubmissionFormset = NewSubmissionFormset(prefix='newSolutions',
                                                    queryset=AssignmentKeeper.objects.filter(
                                                        userSolution__in=newSubmissions).order_by('userSolution__solutionInstance'))

        context['newSubmissionsFormset'] = newSubmissionFormset
        context['solutionInstances'] = solutionInstances
        return context

    def post(self, request, *args, **kwargs):
        newSolutionFormset = NewSolutionFormset(request.POST, prefix='newSolutions')
        newSubmissions = UserSolution.objects.filter(evaluated__isnull=True).filter(
            assignmentkeeper__coach__isnull=True).filter(
            coachReview__isnull=True).filter(userOwner__is_active=True).distinct()
        # solutionInstances = SolutionRouter.objects.filter(usersolution__in=newSubmissions).order_by('usersolution__challengeName__challengeGroupChoices')
        asd = AssignmentKeeper.objects.filter(userSolution__in=newSubmissions).exclude(evaluator__isnull=True)
        if newSolutionFormset.is_valid():
            newSolutionFormset.save()
            for form in newSolutionFormset:
                f = form.instance
                if f.evaluator:
                    evaluatorAssigned(f)
                elif not f.evaluator and f.coach:
                    evaluatorAssigned(f)
            return self.form_valid(newSolutionFormset)
        else:
            print(newSolutionFormset.errors)
            return render(request, 'centralDispatch/newSolutionDispatch.html', {"newSubmissionFormset": newSolutionFormset})


class AssignedSolutions(ListView):
    template_name = 'rubrics/eval_list.html'
    queryset = UserSolution.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssignedSolutions, self).get_context_data()
        if self.request.user.profile.role == 1:
            tc = UserSolution.objects.all().filter(userOwner=self.request.user)
            context['userSolutions'] = tc

        elif self.request.user.profile.role == 2:
            evaluator = UserSolution.objects.all().filter(assignmentkeeper__evaluator=self.request.user.profile)
            if UserSolution.objects.all().filter(evaluated__whoEvaluated=self.request.user).exists():
                pastEvals = UserSolution.objects.all().filter(evaluated__whoEvaluated=self.request.user)
                context['userSolutions'] = evaluator | pastEvals
            else:
                context['userSolutions'] = evaluator

        elif self.request.user.profile.role == 3:
            coach = UserSolution.objects.all().filter(assignmentkeeper__coach=self.request.user.profile)
            topic = UserSolution.objects.all().filter(userOwner__profile__subjectMatter=self.request.user.profile.subjectMatter)
            if UserSolution.objects.all().filter(evaluated__whoEvaluated=self.request.user).exists():
                pastEvals = UserSolution.objects.all().filter(evaluated__whoEvaluated=self.request.user)
                context['userSolutions'] = coach | pastEvals | topic
            else:
                context['userSolutions'] = coach | topic

        elif self.request.user.profile.role == 4:
            everyone = UserSolution.objects.all()
            context['userSolutions'] = everyone

        return context


class SolutionTracker(SingleTableMixin, FilterView, ListView):
    template_name = 'centralDispatch/solutiontracker.html'
    model = SolutionStatus
    table_class = SolutionTable
    table_pagination = {'per_page': 100}
    queryset = SolutionStatus.objects.filter(userSolution__userOwner__is_active=True)
    filterset_class = SolutionTrackerFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SolutionTracker, self).get_context_data(**kwargs)
        context['filter'] = SolutionTrackerFilter
        context['solutionInstances'] = SolutionInstance.objects.all().order_by('challenge_that_owns_me')
        return context


class ChallengeTracker(SingleTableView):
    template_name = 'centralDispatch/solutiontracker.html'
    model = ChallengeStatus
    table_class = ChallengeTable
    # table_data = ChallengeStatus.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChallengeTracker, self).get_context_data(**kwargs)
        context['solutionInstances'] = SolutionInstance.objects.all().order_by('challenge_that_owns_me')
        # thing = SolutionStatus.objects.filter(challengestatus__solutionStatusByInstance__challengestatus=)
        return context


class HackingAboutPage(ListView):
    model = ChallengeStatus
    queryset = ChallengeStatus.objects.all()
    template_name = 'centralDispatch/hackingabout.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HackingAboutPage, self).get_context_data(**kwargs)

        completed = UserSolution.objects.filter(solutionstatus__solutionCompleted=True)
        context['completed'] = completed

        return context
