from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from Long.views import change_password
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change/password/', change_password, name='change_password'),
    path('open/card/', views.OpenCardView.as_view(), name='open_card_form'),
    path('open/account/', views.OpenAccountView.as_view(), name='open_account_form'),
    path('search/customer/', views.SearchCustomerView.as_view(), name='search_customer'),
    path('show/account/', views.show_profile_account, name='show_acc'),
    path('update/<slug:id_cus>/customer/', views.update_profile_customer, name='update_customer'),
    path('search/atm/', views.search_atm, name='atm_search'),
    path('search/atm/<slug:atm_id>/', views.atm_profile, name='atm_profile'),
    path('lock/success/<slug:account_no>', views.lock_account, name='lock_acc'),
    path('open/success/<slug:account_no>', views.open_acc, name='open_acc'),
    path('acc/current/<slug:trans_id>/', views.show_trans_account, name='trans'),
    path('atm/history/<slug:atm_id>', views.show_history_money_detail, name='history_atm'),
    path('atm/update/<slug:atm_id>/<slug:branch_id>/', views.update_profile_atm, name='update_atm'),
    path('customer/api/', views.CustomerRudView.as_view(), name='api_customer'),
    path('account/api/<slug:customer_id>', views.AccountReview, name='account_api'),

    path('employee/<slug:employee_id>/', views.EmployeeView.as_view(), name='employee'),
    path('employee_listview/', views.EmployeeListView.as_view(), name='employee_listview'),
    path('employee_detail/<slug:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    # re_path(r'^employee(?P<slug:pk>)/$', views.EmployeeDetailView.as_view(), name='employee_detail')

    path('customer/detail/<slug:pk>/', views.DetailCustomerView.as_view(), name='detail_customer_view')
]
