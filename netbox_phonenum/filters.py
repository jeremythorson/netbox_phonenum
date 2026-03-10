import django_filters
from django.db.models import Q

from circuits.models import Provider
from dcim.models import Region, Site
from extras.filters import TagFilter
from netbox.filtersets import BaseFilterSet
from tenancy.models import Tenant
from .models import VoiceCircuit, Pool,Number


class PoolFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__id',
        to_field_name='id',
        label='Tenant (id)',
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__id',
        to_field_name='id',
        label='Region (id)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site__id',
        to_field_name='id',
        label='Site (id)',
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        field_name='provider__id',
        to_field_name='id',
        label='Region (id)',
    )
    forward_to = django_filters.ModelMultipleChoiceFilter(
        field_name='forward_to',
        queryset=Pool.objects.all(),
        to_field_name='pk',
        label='forward_to',
    )
    tags = TagFilter(to_field_name='slug', field_name='tags__slug')

    class Meta():
        model = Pool
        fields = ('end', 'start', 'parent', 'tags')

    def search(self, queryset, start, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(start__icontains=value) | Q(end__icontains=value)
        )


class VoiceCircuitFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    name = django_filters.ModelMultipleChoiceFilter(
        field_name='name',
        queryset=VoiceCircuit.objects.all(),
        to_field_name='name',
        label='name',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__id',
        to_field_name='id',
        label='Tenant (id)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site__id',
        to_field_name='id',
        label='Site (id)',
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__id',
        to_field_name='id',
        label='Region (id)',
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        field_name='provider__id',
        to_field_name='id',
        label='Provider (id)',
    )
    tag = TagFilter()

    class Meta():
        model = VoiceCircuit
        fields = ('name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


class NumberFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    name = django_filters.ModelMultipleChoiceFilter(
        field_name='name',
        queryset=Number.objects.all(),
        to_field_name='name',
        label='name',
    )
    
    pool = django_filters.ModelChoiceFilter(
        field_name='pool',
        queryset=Pool.objects.all(),
        label='Pool',
    )

    tenant = django_filters.ModelChoiceFilter(
        field_name='pool__tenant',
        queryset=Tenant.objects.all(),
        label='Tenant',
    )

    description = django_filters.ModelMultipleChoiceFilter(
        queryset=Number.objects.all(),
        field_name='description',
        to_field_name='description',
        label='description',
    )
    
    pool_id = django_filters.ModelMultipleChoiceFilter(
        field_name='pool',
        queryset=Pool.objects.all(),
        to_field_name='id',
        label='Pool (IDs)',
    )

    class Meta():
        model = Number
        fields = ('name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )
