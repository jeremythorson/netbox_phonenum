from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from . import serializers
from .. import filters
from ..models import VoiceCircuit, Pool, Number


class phonenumPluginRootView(APIRootView):
    """
    netbox_phonenum API root view
    """
    def get_view_name(self):
        return 'phonenum'

class PoolViewSet(NetBoxModelViewSet):
    queryset = Pool.objects.prefetch_related('tenant', 'region', 'tags')
    serializer_class = serializers.PoolSerializer
    filterset_class = filters.PoolFilterSet

class VoiceCircuitsViewSet(NetBoxModelViewSet):
    queryset = VoiceCircuit.objects.prefetch_related('tenant', 'region', 'tags')
    serializer_class = serializers.VoiceCircuitSerializer
    filterset_class = filters.VoiceCircuitFilterSet

class NumberViewSet(NetBoxModelViewSet):
    queryset = Number.objects.prefetch_related('pool')
    serializer_class = serializers.NumberSerializer
    filterset_class = filters.NumberFilterSet
