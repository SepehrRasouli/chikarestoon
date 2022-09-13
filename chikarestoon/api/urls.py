from django.urls import path
from rest_framework import routers
from .views import IdeaViewSet,StarViewSet,ProfileViewSet,CommentViewSet,RandomIdeaViewSet
router = routers.SimpleRouter()
router.register(r'idea', IdeaViewSet,basename="idea")
router.register(r'profile',ProfileViewSet,basename='profile')
router.register('comment',CommentViewSet,basename='comment')
urlpatterns = [
    path('star/',StarViewSet.as_view({'get':'get'})),
    path(
        'star/retrieve/<int:pk>/',
        StarViewSet.as_view({'get':'retrieve','patch':'partial_update'})),
    path('idea/random/',RandomIdeaViewSet.as_view({'get':'get'}))
]

urlpatterns += router.urls
