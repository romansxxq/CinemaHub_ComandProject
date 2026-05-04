from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, UserRegisterView, UserProfileView,
    MovieViewSet, HallTypeViewSet, HallViewSet,
    SessionViewSet, BookingViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'hall-types', HallTypeViewSet, basename='hall-type')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
]
