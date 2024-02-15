from rest_framework.routers import DefaultRouter

from reports.api.views import ReportViewSet

app_name = 'reports'

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = router.urls
