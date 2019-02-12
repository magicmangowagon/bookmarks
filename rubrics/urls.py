from django.urls import path
from . import views
from .views import challenge_detail, ChallengeListView, SolutionDetailView, SolutionListView, RubricFormView, EvalDetailView, EvalListView, RubricFinalFormView, CompetencyView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('', ChallengeListView.as_view(), name='challenges'),
    path('challenge/<int:pk>', login_required(challenge_detail.as_view()), name='challenge-detail'),
    # path('challenge/<int:pk>/upload', views.solution_submission, name='solution'),
    path('challenge/<int:pk>/success', views.success, name='success'),
    path('solutions', login_required(SolutionListView.as_view()), name='solutions'),
    path('solutions/<int:pk>', login_required(SolutionDetailView.as_view()), name='solution-detail'),
    path('solutionEval/<int:pk>', login_required(RubricFormView.as_view()), name='solution-eval'),
    path('evals', login_required(EvalListView.as_view()), name='eval-list'),
    path('evals/<int:pk>', login_required(EvalDetailView.as_view()), name='eval-detail'),
    path('solutionEval/end/<int:pk>', login_required(RubricFinalFormView.as_view()), name='solution-end-eval'),
    path('competency', login_required(CompetencyView.as_view()), name='competency-list'),
    # path('edit/', views.edit, name='edit'),
]
