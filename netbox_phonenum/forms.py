import logging
from django import forms
from django.utils.translation import gettext_lazy as _

from circuits.models import Provider
from dcim.models import Region, Site, Device, Interface
from extras.models import Tag
from netbox.forms import NetBoxModelForm
from tenancy.models import Tenant
from utilities.forms import BulkEditForm, CSVModelForm
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField, DynamicModelChoiceField,
    TagFilterField, CSVModelChoiceField
)
from utilities.forms.rendering import FieldSet
from virtualization.models import VirtualMachine, VMInterface
from .choices import VoiceCircuitTypeChoices
from .models import VoiceCircuit, Pool, Number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddRemoveTagsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add add/remove tags fields
        self.fields['add_tags'] = DynamicModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            required=False
        )
        self.fields['remove_tags'] = DynamicModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            required=False
        )


class PoolFilterForm(forms.Form):
    model = Pool
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet(
            "start",
            "end",
            'status',
            'is_pool',
            name=_('Pool')
        ),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
    )
    tags = TagFilterField(model)


class PoolEditForm(NetBoxModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'title': 'Enter name pool'
            }
        )
    )
    start = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'pattern': r'^\+?[0-9A-D\*\#]+$',
                'title': 'Enter the Phone Number'
            }
        )
    )
    end = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'pattern': r'^\+?[0-9A-D\*\#]+$',
                'title': 'Enter the Phone Number'
            }
        )
    )
    parent = DynamicModelChoiceField(queryset=Pool.objects.all(), required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Pool
        fields = ('name', 'start', 'end', 'parent', 'tenant', 'site', 'region', 'description', 'provider', 'forward_to',
                  'tags')


class PoolBulkEditForm(AddRemoveTagsForm, BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Pool.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )

    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    # Implement plugin API to migrate to DynamicModelChoiceField
    forward_to = forms.ModelChoiceField(
        queryset=Pool.objects.all(),
        to_field_name="pk",
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )

    class Meta:
        nullable_fields = ('region', 'site', 'provider', 'forward_to', 'description')


class PoolCSVForm(CSVModelForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text='Assigned tenant'
    )
    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Originating provider'
    )
    region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Assigned region'
    )
    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Assigned site'
    )
    forward_to = CSVModelChoiceField(
        queryset=Pool.objects.all(),
        to_field_name="pk",
        required=False
    )

    class Meta:
        model = Pool
        fields = Pool.csv_headers
        help_texts = {
            'forward_to': "Optional call forwarding Number",
        }


class VoiceCircuitEditForm(NetBoxModelForm):
    name = forms.CharField(
        required=True,
    )
    voice_circuit_type = forms.ChoiceField(
        choices=VoiceCircuitTypeChoices,
        widget=forms.Select(attrs={"onChange": 'ShowVCTypeRelatedDetails();'})
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        initial_params={
            'interfaces': '$interface'
        }
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        query_params={
            'device_id': '$device'
        }
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        initial_params={
            'interfaces': '$vminterface'
        }
    )
    vminterface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        label='Interface',
        query_params={
            'virtual_machine_id': '$virtual_machine'
        }
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Media:
        js = ('netbox_phonenum/js/edit_virtual_circuit.js',)

    class Meta:
        model = VoiceCircuit
        fields = (
            'name', 'voice_circuit_type', 'tenant', 'region', 'site',
            'description', 'provider', 'provider_circuit_id', 'tags',
            'sip_source', 'sip_target'
        )

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is Interface:
                initial['interface'] = instance.assigned_object
            elif type(instance.assigned_object) is VMInterface:
                initial['vminterface'] = instance.assigned_object

        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Cannot select both a device interface and a VM interface
        if self.cleaned_data.get('interface') and self.cleaned_data.get('vminterface'):
            raise forms.ValidationError("Cannot select both a device interface and a virtual machine interface")
        if not (self.cleaned_data.get('interface') or self.cleaned_data.get('vminterface')):
            raise forms.ValidationError("Voice Circuit must be attached to a device interface or a VM interface")
        self.instance.assigned_object = self.cleaned_data.get('interface') or self.cleaned_data.get('vminterface')


class VoiceCircuitFilterForm(forms.Form):
    model = VoiceCircuit
    q = forms.CharField(
        required=False,
        label='Search'
    )
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    provider = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    tags = TagFilterField(model)


class VoiceCircuitBulkEditForm(AddRemoveTagsForm, BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VoiceCircuit.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )

    class Meta:
        nullable_fields = ('region', 'provider', 'description')


class VoiceCircuitCSVForm(CSVModelForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text='Assigned tenant'
    )
    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Originating provider'
    )
    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Assigned site'
    )
    region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Assigned region'
    )
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Parent device of assigned interface (if any)'
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Parent VM of assigned interface (if any)'
    )
    interface = CSVModelChoiceField(
        queryset=Interface.objects.none(),  # Can also refer to VMInterface
        required=True,
        to_field_name='name',
        help_text='Assigned interface'
    )

    class Meta:
        model = VoiceCircuit
        fields = [
            'name', 'voice_circuit_type', 'tenant', 'region', 'site',
            'description', 'provider', 'provider_circuit_id', 'device',
            'virtual_machine', 'interface',
        ]


class NumberEditForm(NetBoxModelForm):

    pool = DynamicModelChoiceField(queryset=Pool.objects.all(), required=True)
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'title': 'Enter numer name'
            }
        )
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'title': 'Enter numer desc'
            }
        )
    )
    class Media:
        js = ('netbox_phonenum/js/edit_virtual_circuit.js',)

    class Meta:
        model = Number
        fields = ('pool', 'name','description')
    
    def clean(self):
        super().clean()
        cleaned = self.cleaned_data or {}

        pool = cleaned.get("pool") or getattr(self.instance, "pool", None)
        name = cleaned.get("name")

        if not pool or name in (None, ""):
            return cleaned

        try:
            numeric_value = int(str(name).strip())
        except (TypeError, ValueError):
            self.add_error("name", "Name must be a valid integer.")
            return cleaned

        start_raw = getattr(pool, "start", None)
        end_raw = getattr(pool, "end", None)
        if start_raw is None or end_raw is None:
            raise ValidationError("Selected pool has no defined start/end range.")

        try:
            start = int(str(start_raw).strip())
            end = int(str(end_raw).strip())
        except (TypeError, ValueError):
            raise ValidationError(
                f"Selected pool has non-numeric start/end values (start={start_raw!r}, end={end_raw!r})."
            )

        if start > end:
            raise ValidationError("Selected pool has invalid range (start > end).")

        if not (start <= numeric_value <= end):
            self.add_error(
                "name",
                f"Number ({numeric_value}) must be within pool range {start}–{end} (inclusive)."
            )

        return cleaned

class NumberCSVForm(CSVModelForm):
    class Meta:
        model = Number
        fields = [
            'name','description','pool']

class NumberBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Number.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
  
    description = forms.CharField(
        max_length=200,
        required=False
    )

    class Meta:
        nullable_fields = ('description')

class NumberFilterForm(forms.Form):
    model = Number
    q = forms.CharField(
        required=False,
        label='Search'
    )
  
    pool = DynamicModelMultipleChoiceField(
        queryset=Pool.objects.all(),
        required=False,
        label='Pool',
        to_field_name='id',
        null_option='None',
    )

    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )