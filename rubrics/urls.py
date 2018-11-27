from django.urls import path
from . import views
from .views import challenge_detail, ChallengeListView

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('', views.ChallengeListView.as_view(), name='challenges'),
    path('challenge/<int:pk>', challenge_detail.as_view(), name='challenge-detail'),
    path('challenge/<int:pk>/upload', views.solution_submission, name='solution'),
    # path('edit/', views.edit, name='edit'),
]
