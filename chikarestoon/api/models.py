from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import  receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_username()
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Idea(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.content

class Star(models.Model):
    stars = models.BigIntegerField(default=0)
    related_idea = models.OneToOneField(Idea, on_delete=models.CASCADE)
@receiver(post_save, sender=Idea)
def create_star_object(sender, instance, created, **kwargs):
    if created:
        Star.objects.create(stars=0,related_idea=instance)

@receiver(post_save,sender=Idea)
def save_star_object(sender,instance,**kwargs):
    instance.star.save()


class StarredIdeas(models.Model):
    related_idea = models.OneToOneField(Idea,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    related_idea = models.ForeignKey(Idea,on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
