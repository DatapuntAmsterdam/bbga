# from django.shortcuts import render

# Create your views here.
from datetime import date

from datapunt_api import rest
from django_filters.rest_framework import filters
from django_filters.rest_framework.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, serializers


@api_view(['GET'])
def meta_groepen(_request):
    """
    Lijst van groepen
    """

    queryset = models.Meta.objects.values('groep').distinct().extra(
        order_by=['groep'])

    data = {
        'groepen': sorted([r['groep'] for r in queryset])
    }
    return Response(data)


@api_view(['GET'])
def meta_themas(_request):
    """
    Lijst met gebruikte thema's
    """
    queryset = models.Meta.objects.values('thema').distinct().extra(
        order_by=['thema'])
    data = {
        'themas': sorted([r['thema'] for r in queryset])
    }
    return Response(data)


@api_view(['GET'])
def meta_variabelen(_request):
    """
    Lijst met gebruikte variabelen
    """
    queryset = models.Meta.objects.values('variabele').distinct().extra(
        order_by=['variabele'])

    data = {
        'variabelen': [r['variabele'] for r in queryset]
    }
    return Response(data)


@api_view(['GET'])
def meta_gebiedcodes(_request):
    """
    Lijst met gebruikte gebiedscodes
    """
    queryset = models.Cijfers.objects.values('gebiedcode15').distinct().extra(
        order_by=['gebiedcode15'])

    data = {
        'variabelen': [r['gebiedcode15'] for r in queryset]
    }
    return Response(data)


class MetaViewSet(rest.DatapuntViewSet):
    """
    Metadata

    Lijst met alle Meta-data gebruikt in BBGA
    """

    queryset = models.Meta.objects.all().order_by('id')
    serializer_class = serializers.Meta
    serializer_detail_class = serializers.MetaDetail
    filter_backends = (DjangoFilterBackend,)

    filter_fields = ('id', 'thema', 'variabele', 'groep', 'bron')


GEBIED_CODES = (
    models.Cijfers.objects
    .values_list('gebiedcode15')
    .distinct()
    .extra(order_by=['gebiedcode15'])
)


class CijfersFilter(FilterSet):
    """
    Filter nummeraanduidingkjes
    """

    jaar = filters.CharFilter(method='filter_jaar', )

    gebiedcode = filters.ChoiceFilter(
        label='gebiedscode',
        method='filter_gebied', choices=[(g[0], g[0]) for g in GEBIED_CODES])

    jaar__gte = filters.NumberFilter(
        field_name='jaar', lookup_expr='gte', label='From year')

    jaar__lte = filters.NumberFilter(
        field_name='jaar', lookup_expr='lte', label='To year')

    class Meta:
        model = models.Cijfers
        fields = [
            'gebiedcode15',
            'gebiedcode',
            'variabele',
            # must be last!!
            'jaar',
        ]

    def filter_gebied(self, queryset, _name, value):
        """filter on gebied code.
        """
        return queryset.filter(gebiedcode15=value)

    def filter_jaar(self, queryset, _name, value):
        """
        Get the latest, or latest x years
        """
        qs = queryset.order_by('-jaar')

        if value == 'latest':
            value = -1

        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError(
                '"jaar" must be "latests" or integer')

        if value < 0:
            years = qs.distinct('jaar').values_list('jaar', flat=True)[:abs(value)]

            return qs.filter(jaar__in=years)

        return queryset.filter(jaar=value)


class CijfersViewSet(rest.DatapuntViewSet):
    """
    Basisbestand Gebieden Amsterdam

    https://www.ois.amsterdam.nl/online-producten/basisbestand-gebieden-amsterdam

    bronhouder: OIS (Onderzoek, Informatie en Statistiek)

    bekijk de filter opties
    er kan op jaar, gebiedcode15 en variabele gefiltert worden

    voorbeeld:

    https://acc.api.data.amsterdam.nl/bbga/cijfers/?variabele=BEV12_17&gebiedcode15=STAD&jaar=2015

    Jaar kan "latest" zijn. maar kan ook -5 zijn voor de laatste 5 jaar.

    """

    queryset = models.Cijfers.objects.all().order_by('-jaar')
    serializer_class = serializers.Cijfers
    serializer_detail_class = serializers.CijferDetail
    filter_class = CijfersFilter
    filter_backends = (DjangoFilterBackend,)

    ordering_fields = ('jaar', 'buurt', 'variabele')
    ordering = ('-jaar', 'buurt', 'variabele')
