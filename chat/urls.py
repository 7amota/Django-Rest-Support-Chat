from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TicketsViewset
router = DefaultRouter()
router.register('tickets',TicketsViewset)
urlpatterns = [
]+ router.urls
