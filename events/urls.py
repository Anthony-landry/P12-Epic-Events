from django.urls import path, include

from events.views import EventViewSet  # viewsets

from rest_framework.routers import DefaultRouter # router


router = DefaultRouter()
router.register("", EventViewSet, basename='events')

urlpatterns = [

    path('events/', include(router.urls))

]