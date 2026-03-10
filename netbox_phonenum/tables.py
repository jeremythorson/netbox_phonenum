import django_tables2 as tables

from netbox.tables import BaseTable, columns
from .models import VoiceCircuit, Pool, Number

ToggleColumn = columns.ToggleColumn


class PoolTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    start = tables.LinkColumn()
    end = tables.LinkColumn()
    parent = tables.LinkColumn()
    tenant = tables.LinkColumn()
    region = tables.LinkColumn()

    site = tables.LinkColumn()
    provider = tables.LinkColumn()
    forward_to = tables.LinkColumn()
    tags = columns.TagColumn()

    class Meta(BaseTable.Meta):
        model = Pool
        fields = ('pk', 'name', 'start', 'end', 'parent', 'tenant', 'site', 'region', 'description', 'provider',
                  'forward_to', 'tags')


class VoiceCircuitTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    voice_device_or_vm = tables.Column(
        accessor='assigned_object.parent_object',
        linkify=True,
        orderable=False,
        verbose_name='Device/VM'
    )
    voice_circuit_type = tables.LinkColumn()
    tenant = tables.LinkColumn()
    region = tables.LinkColumn()
    site = tables.LinkColumn()
    provider = tables.LinkColumn()
    tags = columns.TagColumn()

    class Meta(BaseTable.Meta):
        model = VoiceCircuit
        fields = ('pk', 'name', 'voice_device_or_vm', 'voice_circuit_type', 'tenant', 'region', 'site', 'provider',
                  'tags')


class NumberTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    description = tables.LinkColumn()
    pool = tables.LinkColumn()
    
    tenant = tables.Column(
        accessor='pool.tenant',
        linkify=True,
        verbose_name='Tenant',
        order_by=('pool__tenant__name',),
    )

    site = tables.Column(
        accessor='pool.site',
        linkify=True,
        verbose_name='Site',
        order_by=('pool__site__name',),
    )


    class Meta(BaseTable.Meta):
        model = Number
        fields = ('pk', 'name', 'description', 'pool', 'tenant', 'site')