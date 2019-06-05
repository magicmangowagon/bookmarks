from django.urls import path
from . import views
from .views import ChallengeDetail, ChallengeListView, SolutionDetailView, SolutionListView, RubricFormView, \
    EvalDetailView, EvalListView, RubricFinalFormView, CompetencyView, RubricAddendum, PreEvaluationUpdate, LearningExperienceCreator
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('', ChallengeListView.as_view(), name='challenges'),
    path('challenge/<int:pk>', login_required(ChallengeDetail.as_view()), name='challenge-detail'),
    # path('challenge/<int:pk>/upload', views.solution_submission, name='solution'),
    path('challenge/<int:pk>/success', views.success, name='success'),
    path('solutions', login_required(SolutionListView.as_view()), name='solutions'),
    path('solutions/<int:pk>', login_required(SolutionDetailView.as_view()), name='solution-detail'),
    path('solutionEval/<int:pk>', login_required(RubricFormView.as_view()), name='solution-eval'),
    path('customRubric/<int:pk>', login_required(RubricAddendum.as_view()), name='custom-eval'),
    path('evals', login_required(EvalListView.as_view()), name='eval-list'),
    path('evals/<int:pk>', login_required(EvalDetailView.as_view()), name='eval-detail'),
    path('solutionEval/end/<int:pk>', login_required(RubricFinalFormView.as_view()), name='solution-end-eval'),
    path('competency', login_required(CompetencyView.as_view()), name='competency-list'),
    path('preevaluation/<int:pk>', login_required(PreEvaluationUpdate.as_view()), name='pre-evaluation'),
    path('learningExperience/<int:pk>', LearningExperienceCreator.as_view(), name='learningExperience'),
    # path('edit/', views.edit, name='edit'),
]
