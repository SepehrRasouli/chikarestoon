import random
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.http.response import Http404
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Idea,Star,StarredIdeas,Profile,Comment
from .permissions import IsUserChangingTheirOwnProfile,IsTheUserDoingActionsOnTheirOwnProfile
from .serializers import IdeaSerialiser,StarSerialiser,ProfileSerialiser,UserSerialiser,CommentSerialiser
# Create your views here.

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerialiser
    permission_classes = [IsTheUserDoingActionsOnTheirOwnProfile]

class RandomIdeaViewSet(viewsets.ViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerialiser
    def get(self,request):
        import ipdb;ipdb.set_trace()
        queryset = random.choice(Idea.objects.all())
        serializer_class = IdeaSerialiser(queryset)
        return Response(serializer_class.data)



class StarViewSet(viewsets.ViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerialiser

    @staticmethod
    def de_star(request,pk,idea_object):
        import ipdb;ipdb.set_trace()
        star_obj = Star.objects.get(
            related_idea=pk
        )
        star_obj.stars -= 1
        star_obj.save()
        StarredIdeas.objects.get(
            user=request.user.profile
        ).delete()

    def get(self,request,pk=None) -> Response:
        queryset = Star.objects.all()
        serializer = StarSerialiser(
            queryset,
            many=True,
        )
        return Response(serializer.data)

    def retrieve(self,request,pk=None) -> Response:
        star_object = get_object_or_404(Star,pk=pk)
        serializer = StarSerialiser(star_object)
        return Response(serializer.data)

    def partial_update(self,request,pk=None):
        star_object = get_object_or_404(
            Star,
            pk=pk,
        )
        idea_object = get_object_or_404(
            Idea,
            pk=pk,
        )
        serializer = StarSerialiser(
            star_object,
            data=request.data,
            partial=True,
            context={
                'request':request,
                'pk':pk,
                'idea_object':idea_object,
            }
        )
        import ipdb;ipdb.set_trace()
        if serializer.is_valid(raise_exception=True):
            import ipdb;ipdb.set_trace()
            if serializer.validated_data.get('de_star'):
                self.de_star(request,pk,idea_object)
                return Response({'status':'decreamented by one.'})
            #FIXME: Serializer returns old values, fix it
            star_obj = Star(
                id=pk,
                stars=int(request.data['stars']),
                related_idea=idea_object,
            )
            star_obj.save()
            starredidea_obj = StarredIdeas(
                related_idea=idea_object,
                user=request.user.profile
            )
            starredidea_obj.save()
            return Response(
                serializer.data
            )
        return Response({'status':'bad_request'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerialiser
    permission_classes = [IsUserChangingTheirOwnProfile]
    http_method_names = ['get','head','put','patch']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerialiser
    permission_classes = [IsTheUserDoingActionsOnTheirOwnProfile]
