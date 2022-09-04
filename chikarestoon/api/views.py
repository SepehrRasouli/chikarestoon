from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Idea
from .serializers import IdeaSerialiser
# Create your views here.

class IdeaListView(ListCreateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerialiser
