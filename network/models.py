from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(max_length=256)
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="creator")
    likes = models.ManyToManyField("User", related_name="likes", blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    
    class Meta:
        unique_together = ("follower", "followed")
