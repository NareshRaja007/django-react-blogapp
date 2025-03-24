from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='user-list'),
    path('all_posts', ViewAllPosts.as_view(), name='all_posts'),
    path('post_create', BlogPostCreateView.as_view(), name='post_create'),
    path('my_posts', BlogPostCreateView.as_view(), name='my_posts'),
    path('post_edit', BlogPostCreateView.as_view(), name='post_edit'),
    path('post_delete', BlogPostCreateView.as_view(), name='post_delete'),





    
]