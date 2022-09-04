from rest_framework import serializers
from .models import Idea
class IdeaSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = "__all__"
