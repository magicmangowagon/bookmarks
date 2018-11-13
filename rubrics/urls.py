from django.urls import path
from . import views

urlpatterns = [
    path('rubrics', views.update_challenge, name='challenge-form'),
    path('', views.ChallengeListView.as_view(), name='challenges'),
    path('rubrics/challenge/<int:pk>', views.challenge_detail, name='challenge-detail'),
    # path('edit/', views.edit, name='edit'),
]
