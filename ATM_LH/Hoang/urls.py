from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_url'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.signup_view, name='register'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    # path('withdrawal/another/', views.another_view, name='another'),
]
