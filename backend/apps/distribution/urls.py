from rest_framework.routers import DefaultRouter
from .views import ScheduledPostViewSet

router = DefaultRouter()
router.register(r"scheduler", ScheduledPostViewSet, basename="scheduledpost")
urlpatterns = router.urls
