from rest_framework.routers import DefaultRouter

from areas.api.views import AreaViewSet, CategoryViewSet, CommentViewSet

app_name = 'areas'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
