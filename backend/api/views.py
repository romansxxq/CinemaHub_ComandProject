from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .models import Movie, Genre, Hall, Seat, Session, Booking, HallType
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    GenreSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    HallSerializer,
    HallTypeSerializer,
    SeatSerializer,
    SessionSerializer,
    SessionDetailSerializer,
    BookingCreateSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = None
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = None
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer

    @action(detail=False, methods=['get'])
    def now_showing(self, request):
        """Get movies currently in theaters"""
        movies = Movie.objects.filter(is_now_showing=True)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        """Get movies filtered by genre"""
        genre_id = request.query_params.get('genre_id')
        if not genre_id:
            return Response({'error': 'genre_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        movies = Movie.objects.filter(genres__id=genre_id)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        """Get all sessions for a movie"""
        movie = self.get_object()
        # Get sessions for the next 30 days
        future_date = timezone.now() + timedelta(days=30)
        sessions = Session.objects.filter(
            movie=movie,
            start_time__gte=timezone.now(),
            start_time__lte=future_date
        ).order_by('start_time')
        
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)


class HallTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HallType.objects.all()
    serializer_class = HallTypeSerializer
    permission_classes = (AllowAny,)


class HallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = (AllowAny,)


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    permission_classes = (AllowAny,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['start_time']
    ordering = ['start_time']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SessionDetailSerializer
        return SessionSerializer

    @action(detail=False, methods=['get'])
    def upcoming_sessions(self, request):
        """Get sessions for the next 7 days"""
        today = timezone.now()
        end_date = today + timedelta(days=7)
        
        sessions = Session.objects.filter(
            start_time__gte=today,
            start_time__lte=end_date
        ).order_by('start_time')
        
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingDetailSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Each user can only see their own bookings
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action == 'list':
            return BookingListSerializer
        return BookingDetailSerializer

    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            booking = serializer.save()
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        detail_serializer = BookingDetailSerializer(booking, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get user's active bookings (paid or pending)"""
        bookings = Booking.objects.filter(
            user=request.user,
            status__in=['pending', 'paid'],
            session__start_time__gte=timezone.now()
        ).order_by('session__start_time')
        
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get user's booking history"""
        bookings = Booking.objects.filter(
            user=request.user
        ).order_by('-created_at')
        
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        if booking.status == 'cancelled':
            return Response(
                {'error': 'Booking is already cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.session.start_time <= timezone.now():
            return Response(
                {'error': 'Cannot cancel a session that has already started'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response(
            {'message': 'Booking cancelled successfully'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark booking as paid (for payment integration)"""
        booking = self.get_object()
        booking.status = 'paid'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
