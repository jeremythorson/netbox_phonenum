import importlib.metadata
from netbox.plugins import PluginConfig

class PhoneNumConfig(PluginConfig):
    name = 'netbox_phonenum'
    version = importlib.metadata.version('netbox_phonenum')
    verbose_name = 'PhoneNum Plugin'
    description = 'Telephone Number Management Plugin for NetBox.'
    author = 'Igor Korotchenkov'
    author_email = 'iDebugAll@gmail.com'
    base_url = 'phonenum'
    min_version = "4.4.0"
    max_version = "4.5.99"
    required_settings = []
    default_settings = {}
    caching_config = {
        '*': None
    }

config = PhoneNumConfig
