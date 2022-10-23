from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, token

app_name = 'api'

routers_v1 = DefaultRouter()
routers_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(routers_v1.urls)),
    path('v1/auth/signup/', signup, name="signup"),
    path('v1/auth/token/', token, name='auth_token')
]
