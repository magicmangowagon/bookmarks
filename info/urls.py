from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import BaseInfoList


urlpatterns = [
    path('infolist', BaseInfoList.as_view(), name='infoList')
]
