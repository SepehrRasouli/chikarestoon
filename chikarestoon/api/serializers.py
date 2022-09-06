from rest_framework import serializers
from .models import Idea,Star
class IdeaSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = "__all__"

class StarSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = "__all__"
    def validate_stars(self,value):
        print(value)
        return value

