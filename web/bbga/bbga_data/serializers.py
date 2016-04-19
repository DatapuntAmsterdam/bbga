from rest_framework import serializers

from datapunt_generic.generic import rest
from . import models


class BBGAMixin(rest.DataSetSerializerMixin):
    dataset = 'bbga'


# list serializers
class Meta(serializers.ModelSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Meta


class MetaDetail(BBGAMixin, rest.HALSerializer):

    type = serializers.CharField(source='get_type_display')
    _display = rest.DisplayField()

    class Meta:
        model = models.Meta


class Cijfers(serializers.ModelSerializer):

    class Meta:
        model = models.Cijfers
        fields = (
            'id',
            'jaar',
            'gebiedcode15',
            'variabele',
            'waarde'
        )


class CijferDetail(BBGAMixin, rest.HALSerializer):
    type = serializers.CharField(source='get_type_display')
    _display = rest.DisplayField()

    class Meta:
        model = models.Cijfers


class VariabelenSerializer(serializers.Serializer):
    variabele = serializers.CharField(max_length=50)
