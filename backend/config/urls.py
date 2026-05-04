from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import (
    CustomTokenObtainPairView,
    UserRegisterView,
    UserProfileView,
    MovieViewSet,
    HallTypeViewSet,
    HallViewSet,
    SessionViewSet,
    BookingViewSet,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'hall-types', HallTypeViewSet, basename='hall-type')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('admin/', admin.site.urls),

    # OpenAPI schema + Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API routes
    path('api/', include(router.urls)),
    
    # Authentication routes
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user_profile'),
]
