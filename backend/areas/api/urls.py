from areas.api.views import AreaViewSet, CategoryViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
