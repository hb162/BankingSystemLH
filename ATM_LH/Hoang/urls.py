from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.signup_view, name='register'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('transferin/', views.transfer_internal, name='internal'),
    path('transferex/', views.transfer_external, name='external'),
    path('opencard/', views.open_card, name='opencard'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # path('withdrawal/another/', views.another_view, name='another'),
]
