from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from Long.views import change_password, open_new_card, open_new_account, search_customer_anythings


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change/password/', change_password, name='change_password'),
    path('open/card/', open_new_card, name='open_card'),
    path('open/account/', open_new_account, name='open_account'),
    path('search/', search_customer_anythings, name='search_customer'),
]
