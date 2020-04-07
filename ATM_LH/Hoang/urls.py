from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('account', views.AccountView)
router.register('customer', views.CustomerView)
router.register('card', views.CardView)

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
    path('change_pass/', views.change_pass_view, name='change_pass'),
    path('profile/', views.profile_view, name='profile'),
    path('history/', views.history_view, name='history'),
    path('history/<int:transaction_id>/', views.detail_history, name='detail'),
    path('success/', views.success_view, name='success'),
    path('history/normal_search/', views.normal_search, name='normal_search'),
    # path('history/advanced_search', views.advanced_search, name='advanced_search'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))

]
