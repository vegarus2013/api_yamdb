from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewsViewSet

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
]
