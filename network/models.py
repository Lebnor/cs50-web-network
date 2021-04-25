from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('following',)

class User(AbstractUser):


    def getLikes(self):
        likes = []
        for like in self.liked.all():
            likes.append(like.post.id)
        return sorted(likes)
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            'likes': self.getLikes()
        }
    
    def __str__(self):
        return f"{self.username}"

class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def serialize(self):
        following = []
        for item in self.following.all():
            following.append(item.serialize())
        followers = []
        user_followers = Profile.objects.filter(following=self.user)
        for profile in user_followers:
            followers.append(profile.user.serialize())
        return {
            "user": {
                "id": self.user.id,
                "username": self.user.username
            },
            "following": following,
            "followers": followers
            
        }

class Post(models.Model):
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    likes = models.PositiveIntegerField(default=0, blank=True, null=True)

    def serialize(self):
        return {
            "id": self.pk,
            "poster": {
                "id": self.poster.id,
                "username": self.poster.username
            },
            "text": self.text,
            "likes": self.likes,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f'{self.id}: {self.poster.username}'

class Like(models.Model):
    user = models.ForeignKey(User, related_name="liked", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="like", on_delete=models.CASCADE)

    def serialize(self):
        return {
            'post': self.post.id
        }
    def __str__(self):
        return f"user: {self.user.username}, post: {self.post.id}"

class Comment(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField()
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
