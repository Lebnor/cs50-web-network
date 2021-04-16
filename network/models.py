from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    poster = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts", null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField()
    likes = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "id": self.pk,
            "poster": self.poster.username,
            "text": self.text,
            "likes": self.likes,
            "timestamp": self.timestamp
        }
    def __str__(self):
        return serialize(self)

class Comment(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField()
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)

