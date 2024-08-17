from django.urls import include, path
from rest_framework import routers

from .views import (
    auth_signup,
    auth_token,
    MeViewSet,
    UserViewSet
)


router = routers.DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('auth/signup/', auth_signup),
    path('auth/token/', auth_token, name='token_obtain_pair'),
    path('users/me/', MeViewSet.as_view()),
    path('', include(router.urls)),
]
