from django.urls import path, include
from . import views
from utilities.urls import get_model_urls

app_name = "netbox_phonenum"

urlpatterns = (
    path(
        "pool/",
        include(get_model_urls("netbox_phonenum", "pool", detail=False)),
    ),
    path(
        "pool/<int:pk>/",
        include(get_model_urls("netbox_phonenum", "pool")),
    ),
    path(
        "voicecircuits/",
        include(get_model_urls("netbox_phonenum", "voicecircuit", detail=False)),
    ),
    path(
        "voicecircuits/<int:pk>/",
        include(get_model_urls("netbox_phonenum", "voicecircuit")),
    ),
    path(
        "number/",
        include(get_model_urls("netbox_phonenum", "number", detail=False)),
    ),
    path(
        "number/<int:pk>/",
        include(get_model_urls("netbox_phonenum", "number")),
    ),
)
