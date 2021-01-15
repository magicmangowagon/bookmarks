from django.urls import path
from . import views
from .views import PortfolioUploadView, PortfolioListView, UserPortfolioDetailView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('portfolioUpload/<int:pk>', PortfolioUploadView.as_view(), name='portfolio-upload'),
    path('portfolioupload', PortfolioListView.as_view(), name='portfolios'),
    path('portfoliodetail/<int:pk>', UserPortfolioDetailView.as_view(), name='user-portfolio'),
]
