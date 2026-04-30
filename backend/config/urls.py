from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    CustomTokenObtainPairView,
    UserRegisterView,
    UserProfileView,
    GenreViewSet,
    MovieViewSet,
    HallTypeViewSet,
    HallViewSet,
    SessionViewSet,
    BookingViewSet,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'hall-types', HallTypeViewSet, basename='hall-type')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include(router.urls)),
    
    # Authentication routes
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user_profile'),
]
