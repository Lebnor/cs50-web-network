
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("posts/like/<int:id>", views.like, name="like"),
    path("posts/dislike/<int:id>", views.dislike, name="dislike")
]
