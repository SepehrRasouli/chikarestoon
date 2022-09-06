from django.urls import path,include

#from .views import IdeaViewSet

#urlpatterns = [
#    path("",IdeaViewSet.as_view({'get':'get'}),name="list"),
#    path("stars/",StarListView.as_view(),name="star-list"),
#    path("stars/<int:pk>/",StarUpdateView.as_view(),name="star-update")
#]

from .views import IdeaViewSet,StarViewSet
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'idea', IdeaViewSet,basename="idea")

urlpatterns = [
    path('star/<int:pk>/',StarViewSet.as_view({'post':'create','get':'retrieve'}))
]

urlpatterns += router.urls
