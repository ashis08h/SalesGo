from django.urls import path
from .views import LoginView, DashboardView, SignUpView, PostListView, PostEditView,\
    PostCreateView, PostDeleteView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login', LoginView.as_view(), name='login_view'),
    path('dashboard', DashboardView.as_view(), name='dashboard_view'),
    path('signup', SignUpView.as_view(), name='signup_view'),
    path('logout', LogoutView.as_view(), name='logout_view'),
    path('posts', PostListView.as_view(), name='posts_view'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='edit_post'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post')
]