from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/loans', views.LoanViewSet, basename='loan')
router.register(r'api/countries', views.CountryViewSet, basename='country')
router.register(r'api/sectors', views.SectorViewSet, basename='sector')

urlpatterns = [
    path('', include(router.urls)),
]
