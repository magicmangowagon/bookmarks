from django.urls import path
from . import views

urlpatterns = [
    path('', views.update_challenge, name='challenge'),
    # path('edit/', views.edit, name='edit'),
]
