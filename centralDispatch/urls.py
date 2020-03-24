from .views import NewSolutionDispatch
from django.urls import path
from . import views
from .views import NewSolutionDispatch
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('rubrics', views.update_challenge, name='challenge-form'),
    path('centraldispatch', NewSolutionDispatch.as_view(), name='central-dispatch'),
]
