from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    likes = models.PositiveIntegerField(default=0)

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


class Comment(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField()
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
