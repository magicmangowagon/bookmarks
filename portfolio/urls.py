from django.urls import path
from . import views
from .views import PortfolioUploadView, PortfolioListView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('portfolioUpload/<int:pk>', PortfolioUploadView.as_view(), name='portfolio-upload'),
    path('portfolioupload', PortfolioListView.as_view(), name='portfolios'),
]
