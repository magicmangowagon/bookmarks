from django.shortcuts import render
from rubrics.models import UserSolution, Challenge, Evaluated, SolutionInstance, MegaChallenge
from account.models import Profile
from django.contrib.auth.models import User
from .models import SolutionRouter, ManualAssignmentKeeper
from django.views.generic import ListView, DetailView, FormView
from .forms import SolutionRouterForm, ManualAssignmentKeeperForm
from django.forms import BaseModelFormSet, modelformset_factory


# Create your views here.
class NewSolutionDispatch(ListView):
    context_object_name = 'newSolutions'
    queryset = UserSolution.objects.all().filter(evaluated__isnull=True)
    template_name = 'centralDispatch/newSolutionDispatch.html'

    def get_context_data(self, **kwargs):
        context = super(NewSolutionDispatch, self).get_context_data()
        challenges = MegaChallenge.objects.all().filter(challenge__solutions__isnull=False).distinct().order_by('challengeGroupChoices')
        solutionInstances = SolutionInstance.objects.all().filter(challenge_that_owns_me__megaChallenge__in=challenges)

        SolutionRouterFormset = modelformset_factory(SolutionRouter, extra=0,
                                                     formset=SolutionRouterForm, fields=('coach',
                                                                                         'challenge',
                                                                                         'solutionInstance',
                                                                                         'automate',
                                                                                         'routerChoices'), )
        solutionRouterFormset = SolutionRouterFormset(prefix='routerFormset', queryset=SolutionRouter.objects.all().filter(
            solutionInstance__challenge_that_owns_me__megaChallenge__in=challenges).order_by('challenge__challengeGroupChoices'))

        newSubmissions = UserSolution.objects.all().filter(evaluated__isnull=True)
        NewSubmissionFormset = modelformset_factory(ManualAssignmentKeeper, extra=newSubmissions.count(),
                                                    formset=ManualAssignmentKeeperForm, fields=(
            'coach', 'userSolution'))
        newSubmissionFormset = NewSubmissionFormset(prefix='newSolutions', initial=[{'userSolution': newSubmission.pk}
                                                                                    for newSubmission in newSubmissions],
                                                    queryset=ManualAssignmentKeeper.objects.none())

        context['solutionRouterFormset'] = solutionRouterFormset
        context['challenges'] = challenges
        context['solutionInstances'] = solutionInstances
        context['newSubmissionsFormset'] = newSubmissionFormset
        print(newSubmissions.count())
        return context
