from django.urls import path

from posts import views
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('follow/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow',
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow',
    ),
    path('', views.index, name='index'),
]
