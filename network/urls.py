
from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('admin', admin.site.urls),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow", views.index, name="follow"),
    path("posts", views.posts, name="posts"),
    path("posts/following", views.get_posts_following, name="get_posts_following"),
    path("posts/like/<int:id>", views.like, name="like"),
    path("posts/dislike/<int:id>", views.dislike, name="dislike"),
    path("posts/create/<str:text>", views.create, name="create"),
    path("posts/edit/<int:id>/<str:content>", views.edit, name="edit"),
    path("posts/<str:username>", views.posts_for_user, name="posts_for_user"),
    path("users/get/<str:username>", views.get_user, name="get_user"),
    path("users/follow/<str:username>", views.follow, name="follow"),
    path("users/unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("users/current", views.get_current_user, name="current"),
    path("users/<str:profile>", views.profile, name="profile"),
]
