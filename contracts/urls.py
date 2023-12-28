from django.urls import path, include

from contracts.views import ContractViewSet  # viewsets

from rest_framework.routers import DefaultRouter  # router

router = DefaultRouter()
router.register("", ContractViewSet, basename='contracts')

urlpatterns = [

    path('contracts/', include(router.urls))

]
