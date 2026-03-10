from packaging import version
from django.conf import settings

from netbox.plugins import PluginMenuItem, PluginMenu, PluginMenuButton

plugin_settings = settings.PLUGINS_CONFIG["netbox_phonenum"]


plugin_menu = (
    PluginMenuItem(
        link='plugins:netbox_phonenum:pool_list',
        link_text='Pools',
        permissions=["netbox_phonenum.view_pool"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_phonenum:pool_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_phonenum.add_pool"],
            ),
            PluginMenuButton(
                link="plugins:netbox_phonenum:pool_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
                permissions=["netbox_phonenum.add_pool"],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_phonenum:voicecircuit_list',
        link_text='Voice Circuits',
        permissions=["netbox_phonenum.view_voicecircuit"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_phonenum:voicecircuit_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_phonenum.add_voicecircuit"],
            ),
            PluginMenuButton(
                link="plugins:netbox_phonenum:voicecircuit_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
                permissions=["netbox_phonenum.add_voicecircuit"],
            ),
        ),
    ),

    PluginMenuItem(
        link='plugins:netbox_phonenum:number_list',
        link_text='Numbers',
        permissions=["netbox_phonenum.view_number"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_phonenum:number_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["netbox_phonenum.add_number"],
            ),
        ),
    ),
)

if plugin_settings.get("top_level_menu", True):
    menu = PluginMenu(
        label="Phonenum Plugin",
        groups=(("Voice", plugin_menu),),
        icon_class="mdi mdi-phone-dial",
    )
else:
    menu_items = plugin_menu
