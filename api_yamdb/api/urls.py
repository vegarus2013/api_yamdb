from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

app_name = 'api'

routers_v1 = DefaultRouter()
routers_v1.register(r'users', UserViewSet, basename='users')
routers_v1.register(r'categories', CategoryViewSet, basename='categories')
routers_v1.register(r'genres', GenreViewSet, basename='genres')
routers_v1.register(r'titles', TitleViewSet, basename='titles')

routers_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
routers_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(routers_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='auth_token')
]
