from django.urls import path, include
from . import views
from rest_framework import routers
from django.contrib.auth.decorators import login_required
from .views import BaseInfoList, BaseInfoDetail, DiscussionTopicView, DiscussionBoardView, DesignJournalView, \
    LearningModuleView, LearningModulePage, LearningModuleListView, CaseStudyReview, PromptResponseViewSet

router = routers.DefaultRouter()
router.register(r'prompt-responses', views.PromptResponseViewSet)

urlpatterns = [
    path('infolist', BaseInfoList.as_view(), name='infoList'),
    path('infodetail/<int:pk>', BaseInfoDetail.as_view(), name='infodetail', ),
    path('discussionboard/<int:pk>', login_required(DiscussionBoardView.as_view()), name='discussion-board'),
    path('discussiontopic/<int:pk>', login_required(DiscussionTopicView.as_view()), name='discussion-topic'),
    path('designjournal/<int:pk>', login_required(DesignJournalView.as_view()), name='design-journal'),
    path('learningmodule/<int:pk>', login_required(LearningModuleView.as_view()), name='learning-module', ),
    path('learningmodulepagelist', login_required(LearningModuleListView.as_view()), name='learning-module-pages', ),
    path('casestudyreview/<int:pk>', login_required(CaseStudyReview.as_view()), name='case-study-review', ),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
