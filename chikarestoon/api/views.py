from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Idea,Star,StarredPosts
from .serializers import IdeaSerialiser,StarSerialiser
# Create your views here.

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerialiser

class StarViewSet(viewsets.ViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerialiser
    @staticmethod
    def pk_correspands_to_an_idea_check(pk:int) -> [bool] or [bool,Response]:
        pk_correspands_to_an_idea = bool(
            Idea.objects.filter(
                pk=pk
            )
        )
        if not pk_correspands_to_an_idea:
            return [False,Response(
                {'status':'Article object with the given pk dosen\'t exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )]
        return [True]

    @staticmethod
    def star_object_exists_check(pk:int) -> [bool] or [bool,Response]:
        not_empty = bool(Star.objects.filter(
            related_idea=pk
        ))
        if not_empty:
            return [True,Response(
                {'status':'Can\'t create an already existing star object.'},
                status=status.HTTP_400_BAD_REQUEST
            )]
        return [True]

    def retrieve(self,request,pk=None) -> Response:
        queryset = Star.objects.all()
        star_object = get_object_or_404(queryset,pk=pk)
        serializer = StarSerialiser(star_object)
        return Response(serializer.data)

    def create(self,request,pk=None) -> Response:
        pk_correspands_to_an_idea = self.pk_correspands_to_an_idea_check(pk)
        star_object_exists = self.star_object_exists_check(pk)
        if not pk_correspands_to_an_idea[0]:
            return pk_correspands_to_an_idea[1]
        if star_object_exists[0]:
            return star_object[1]
        else:
            queryset = Star.objects.all()
            serializer = StarSerialiser(queryset,data=request.data,many=True)
            star_obj = Star(stars=int(request.data['stars']),related_idea=Idea.objects.filter(pk=pk)[0])
            star_obj.save()
            return Response(serializer.data) if serializer.is_valid() else Response({})

    def update(self,request,pk=None):
        pass
