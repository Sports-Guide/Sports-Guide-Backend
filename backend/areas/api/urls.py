from rest_framework.routers import DefaultRouter

from areas.api.views import (
    AreaViewSet,
    CategoryViewSet,
    CommentViewSet,
    ReportViewSet,
)

app_name = 'areas'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = router.urls
