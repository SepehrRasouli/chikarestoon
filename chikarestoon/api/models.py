from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Idea(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Star(models.Model):
    stars = models.BigIntegerField(default=0)
    related_idea = models.ForeignKey(Idea,on_delete=models.CASCADE)

class StarredPosts(models.Model):
    starred_idea = models.ForeignKey(Idea,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
