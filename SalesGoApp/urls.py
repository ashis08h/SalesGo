from django.urls import path
from .views import LoginView, DashboardView, SignUpView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login', LoginView.as_view(), name='login_view'),
    path('dashboard', DashboardView.as_view(), name='dashboard_view'),
    path('signup', SignUpView.as_view(), name='signup_view'),
    path('logout', LogoutView.as_view(), name='logout_view')
]