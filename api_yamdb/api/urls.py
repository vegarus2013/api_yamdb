from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import signup, email, token

app_name = 'api'
router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name="token"),
    path('v1/auth/code/', email, name='code'),
]
