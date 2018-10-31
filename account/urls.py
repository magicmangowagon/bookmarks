from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # post views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view, name='password_reset_done'),
    path('reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_view'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view, name='password_reset_complete'),
]
