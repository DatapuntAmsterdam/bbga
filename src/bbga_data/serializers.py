from datapunt_api import rest
from rest_framework import serializers

from . import models


class BBGAMixin(rest.DataSetSerializerMixin):
    dataset = 'bbga'


# list serializers
class MetaSerialiser(serializers.ModelSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Meta
        fields = '__all__'


class MetaDetail(BBGAMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Meta
        fields = '__all__'


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
    _display = rest.DisplayField()

    class Meta:
        model = models.Cijfers
        fields = '__all__'


class VariabelenSerializer(serializers.Serializer):
    variabele = serializers.CharField(max_length=50)
