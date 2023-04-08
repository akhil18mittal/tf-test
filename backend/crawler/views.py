from rest_framework import viewsets
from .models import Loan, Country, Sector
from .serializers import LoanSerializer, CountrySerializer, SectorSerializer


class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
