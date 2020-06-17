from .views import SolutionDispatch
from django.urls import path
from . import views
from .views import SolutionDispatch, NewSolutionDispatch, AssignedSolutions, SolutionTracker, ChallengeTracker
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('centraldispatch', login_required(SolutionDispatch.as_view()), name='central-dispatch'),
    path('centraldispatch/newsolutions', login_required(NewSolutionDispatch.as_view()), name='central-dispatch-new-solutions'),
    path('assignedsolutions', login_required(AssignedSolutions.as_view()), name='assigned-solutions'),
    path('solutiontracker', login_required(SolutionTracker.as_view()), name='solution-tracker'),
    path('challengetracker', login_required(ChallengeTracker.as_view()), name='challenge-tracker')

]
