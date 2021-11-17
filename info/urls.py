from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import BaseInfoList, BaseInfoDetail, DiscussionTopicView, DiscussionBoardView, DesignJournalView


urlpatterns = [
    path('infolist', BaseInfoList.as_view(), name='infoList'),
    path('infodetail/<int:pk>', BaseInfoDetail.as_view(), name='infodetail', ),
    path('discussionboard/<int:pk>', login_required(DiscussionBoardView.as_view()), name='discussion-board'),
    path('discussiontopic/<int:pk>', login_required(DiscussionTopicView.as_view()), name='discussion-topic'),
    path('designjournal/<int:pk>', login_required(DesignJournalView.as_view()), name='design-journal')
]
