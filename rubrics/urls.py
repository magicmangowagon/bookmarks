from django.urls import path
from . import views
from .views import challenge_detail, ChallengeListView, SolutionDetailView, SolutionListView, RubricFormView, EvalDetailView, EvalListView

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('', ChallengeListView.as_view(), name='challenges'),
    path('challenge/<int:pk>', challenge_detail.as_view(), name='challenge-detail'),
    path('challenge/<int:pk>/upload', views.solution_submission, name='solution'),
    path('challenge/<int:pk>/success', views.success, name='success'),
    path('solutions', SolutionListView.as_view(), name='solutions'),
    path('solutions/<int:pk>', SolutionDetailView.as_view(), name='solution-detail'),
    path('solutionEval/<int:pk>', RubricFormView.as_view(), name='solution-eval'),
    path('evals', EvalListView.as_view(), name='eval-list'),
    path('evals/<int:pk>', EvalDetailView.as_view(), name='eval-detail')
    # path('edit/', views.edit, name='edit'),
]
