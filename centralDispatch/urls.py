from .views import SolutionDispatch
from django.urls import path
from . import views
from .views import SolutionDispatch, NewSolutionDispatch, AssignedSolutions, SolutionTracker
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('centraldispatch', SolutionDispatch.as_view(), name='central-dispatch'),
    path('centraldispatch/newsolutions', NewSolutionDispatch.as_view(), name='central-dispatch-new-solutions'),
    path('assignedsolutions', AssignedSolutions.as_view(), name='assigned-solutions'),
    path('solutiontracker', SolutionTracker.as_view(), name='solution-tracker')
]
