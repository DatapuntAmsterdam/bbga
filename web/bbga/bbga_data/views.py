# from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.decorators import api_view

from datapunt_generic.generic import rest
from . import models
from . import serializers


@api_view(['GET'])
def meta_groepen(request):

    queryset = models.Meta.objects.values('groep').distinct().extra(
        order_by=['groep'])

    data = {
        'groepen': sorted([r['groep'] for r in queryset])
    }
    return Response(data)


@api_view(['GET'])
def meta_themas(request):
    queryset = models.Meta.objects.values('thema').distinct().extra(
        order_by=['thema'])
    data = {
        'themas': sorted([r['thema'] for r in queryset])
    }
    return Response(data)


@api_view(['GET'])
def meta_variabelen(request):
    queryset = models.Meta.objects.values('variabele').distinct().extra(
        order_by=['variabele'])

    data = {
        'variabelen': [r['variabele'] for r in queryset]
    }
    return Response(data)


class MetaViewSet(rest.AtlasViewSet):

    queryset = models.Meta.objects.all()
    serializer_class = serializers.Meta
    serializer_detail_class = serializers.MetaDetail
    filter_fields = ('id', 'thema', 'variabele', 'groep', 'bron')

    @list_route(methods=['get'])
    def themas(self, request):
        queryset = models.Meta.objects.values('thema').distinct()
        data = {
            'themas': [r['thema'] for r in queryset]
        }
        return Response(data)

    @list_route(methods=['get'])
    def groepen(self, request):
        queryset = models.Meta.objects.values('groep').distinct()
        data = {
            'groepen': [r['groep'] for r in queryset]
        }
        return Response(data)

    @list_route(methods=['get'])
    def variabelen(self, request):
        queryset = models.Meta.objects.values('variabele').distinct()
        data = {
            'variabelen': [
                r['variabele'] for r in queryset]
        }
        return Response(data)


class CijfersViewSet(rest.AtlasViewSet):

    queryset = models.Cijfers.objects.all()
    serializer_class = serializers.Cijfers
    serializer_detail_class = serializers.CijferDetail
    filter_fields = ('jaar', 'gebiedcode15', 'variabele')
