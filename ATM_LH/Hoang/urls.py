from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.signup_view, name='register'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('withdrawal/another/', views.another_view, name='another'),
    path('transferin/', views.transfer_internal, name='internal'),
    path('transferin/confirm_transfer_in', views.confirm_internal, name='confirm_in'),
    path('transferex/', views.transfer_external, name='external'),
    path('transferex/confirm_transfer_out', views.confirm_external, name='confirm_ex'),
    path('opencard/', views.open_card, name='opencard'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot/', views.forgot_view, name='forgot'),
    path('profile/', views.profile_view, name='profile'),
    path('history/', views.history_view, name='history'),
    path('history/<int:transaction_id>/', views.detail_history, name='detail'),
]
