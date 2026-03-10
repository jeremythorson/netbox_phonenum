from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.APIRootView = views.phonenumPluginRootView

router.register(r'pool', views.PoolViewSet)
router.register(r'voice-circuits', views.VoiceCircuitsViewSet)
router.register(r'numbers', views.NumberViewSet)

app_name = "netbox_phonenum-api"
urlpatterns = router.urls
