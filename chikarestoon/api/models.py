from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Idea(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
