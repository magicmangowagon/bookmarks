from .views import SolutionDispatch
from django.urls import path
from . import views
from .views import SolutionDispatch, NewSolutionDispatch, AssignedSolutions, SolutionTracker, ChallengeTracker, \
    HackingAboutPage, CompetencyTracker, assume_id
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('centraldispatch', login_required(SolutionDispatch.as_view()), name='central-dispatch'),
    path('centraldispatch/newsolutions', login_required(NewSolutionDispatch.as_view()), name='central-dispatch-new-solutions'),
    path('assignedsolutions', login_required(AssignedSolutions.as_view()), name='assigned-solutions'),
    path('solutiontracker', login_required(SolutionTracker.as_view()), name='solution-tracker'),
    path('challengetracker', login_required(ChallengeTracker.as_view()), name='challenge-tracker'),
    path('hackingabout', login_required(HackingAboutPage.as_view()),  name='hackingabout'),
    path('competencytracker', login_required(CompetencyTracker.as_view()), name='competency-tracker'),
    path('assumeuserid', login_required(assume_id), name='assume-id')
]
