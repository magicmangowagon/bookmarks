from django.urls import path
from . import views
from .views import ChallengeDetail, ChallengeListView, SolutionDetailView, SolutionListView, RubricFormView, \
    EvalDetailView, EvalListView, RubricFinalFormView, CompetencyView, RubricAddendum, PreEvaluationUpdate, \
    LearningExperienceCreator, LearningExperienceView, ChallengeCover, CoachingReviewView, SolutionSectionView, \
    MegaSubPage, CoachingReviewSession, searchSubmissions, ChallengeResourcesView, TFJHotFixView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('', ChallengeListView.as_view(), name='challenges'),
    path('challenge/<int:pk>', login_required(ChallengeDetail.as_view()), name='challenge-detail'),
    path('challengeCover/<int:pk>', login_required(ChallengeCover.as_view()), name='challenge-cover'),
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
    path('learningExperienceEdit/<int:pk>', login_required(LearningExperienceCreator.as_view()), name='learningExperienceEdit'),
    path('learningExperience/<int:pk>', login_required(LearningExperienceView.as_view()), name='learningExperience'),
    path('coachingreview/<int:pk>', login_required(CoachingReviewView.as_view()), name='coachingReview'),
    path('coachingsession/<int:pk>', login_required(CoachingReviewSession.as_view()), name='coachingSession'),
    path('solutionsection/<int:pk>', login_required(SolutionSectionView.as_view()), name='solutionSections'),
    path('subsolutions/<int:pk>', login_required(MegaSubPage.as_view()), name='megasolution'),
    path('solutionSearch', login_required(views.searchSubmissions), name='solutionSearch'),
    path('challengeResources/<int:pk>', login_required(views.ChallengeResourcesView.as_view()), name='challengeResources'),
    path('tfj', login_required(TFJHotFixView.as_view()), name='tfj-solutions'),
    # path('edit/', views.edit, name='edit'),
]
