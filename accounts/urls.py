from django.urls import path, include

from accounts.views import UserViewSet, ClientViewSet  # viewsets

from rest_framework.routers import DefaultRouter  # router

router = DefaultRouter()
router.register("users", UserViewSet, basename='users')
router.register("clients", ClientViewSet, basename='clients')

urlpatterns = [

    path('accounts/', include(router.urls))

]
