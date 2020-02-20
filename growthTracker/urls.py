from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from growthTracker import views


urlpatterns = [
    path('growthTracker', views.RubricList.as_view()),
    path('growthTracker/<int:pk>', views.RubricDetail.as_view()),
    path('completedFeedback', views.CompletedFeedback.as_view({'get': 'list'}))
]
