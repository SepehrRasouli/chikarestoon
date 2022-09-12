from rest_framework import serializers
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from .models import Idea,Star,Profile,User,Comment,StarredIdeas
class IdeaSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = "__all__"

class StarSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = "__all__"

    def validate(self,data):
        import ipdb;ipdb.set_trace()
        current_stars = self.instance.stars
        idea_object = self.context.get('idea_object')
        profile = self.context.get("request").user.profile
        pk = self.context.get("pk")
        de_star = False
        if not 'stars' in data.keys():
            raise serializers.ValidationError('You can only change stars field')
        if profile == None:
            raise serializers.ValidationError('User is not authenticated.',code=401)
        if data['stars'] - current_stars > 1:
            raise serializers.ValidationError('You can\'t increament stars more than one.')
        if data['stars'] - current_stars < -1:
            raise serializers.ValidationError('You can\'t decreament stars more than one.')
        try:
            if data['stars'] - current_stars == -1 and \
            get_object_or_404(
                StarredIdeas,
                user=profile,
                related_idea=idea_object
            ).related_idea_id == pk:
                de_star = True
                return {'data':data,'de_star':de_star}
            if get_object_or_404(
                StarredIdeas,
                user=profile,
                related_idea=idea_object
            ).related_idea_id == pk:
                raise serializers.ValidationError('You can\'t star more than once.')
        except Http404:
            pass
        else:
            return {'data':data,'de_star':de_star}

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password','username','first_name','last_name','email')

class ProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class CommentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

