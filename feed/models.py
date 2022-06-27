from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class post(models.Model):
    text = models.TextField(max_length=280, default='')
    datetime = models.DateTimeField(default=timezone.now)
    uname = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    def total_likes(self):
        return self.likes.count()
