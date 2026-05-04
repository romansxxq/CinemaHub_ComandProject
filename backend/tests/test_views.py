import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Movie, Booking
from datetime import datetime, timedelta

User = get_user_model()


@pytest.mark.django_db
class TestUserRegisterView:
    """Test user registration API endpoint"""
    
    def test_register_user_success(self, api_client):
        """Test successful user registration"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'first_name': 'John'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_register_user_password_mismatch(self, api_client):
        """Test registration with mismatched passwords fails"""
        data = {
            'email': 'user@example.com',
            'username': 'user',
            'password': 'password123',
            'password_confirm': 'different123'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_duplicate_email(self, api_client, authenticated_user):
        """Test registration with duplicate email fails"""
        data = {
            'email': 'test@example.com',
            'username': 'anotheruser',
            'password': 'pass123456',
            'password_confirm': 'pass123456'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfileView:
    """Test user profile API endpoints"""
    
    def test_get_profile_authenticated(self, authenticated_client, authenticated_user):
        """Test getting user profile when authenticated"""
        response = authenticated_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'test@example.com'
    
    def test_get_profile_not_authenticated(self, api_client):
        """Test getting user profile without authentication fails"""
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_profile(self, authenticated_client, authenticated_user):
        """Test updating user profile"""
        data = {
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLast'
        }
        response = authenticated_client.patch('/api/auth/profile/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        authenticated_user.refresh_from_db()
        assert authenticated_user.first_name == 'UpdatedName'


@pytest.mark.django_db
class TestMovieViewSet:
    """Test Movie API endpoints"""
    
    def test_list_movies(self, api_client, movie):
        """Test listing movies"""
        response = api_client.get('/api/movies/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_list_movies_now_showing(self, api_client, movie, another_movie):
        """Test listing only now showing movies"""
        response = api_client.get('/api/movies/now_showing/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Test Movie'
    
    def test_retrieve_movie_detail(self, api_client, movie):
        """Test retrieving movie detail"""
        response = api_client.get(f'/api/movies/{movie.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Movie'
        assert response.data['description'] == 'A great test movie'
    
    def test_movie_search(self, api_client, movie):
        """Test searching movies"""
        response = api_client.get('/api/movies/?search=Test')
        assert response.status_code == status.HTTP_200_OK
        assert any(m['title'] == 'Test Movie' for m in response.data)
    
    def test_movie_sessions_endpoint(self, api_client, movie, session):
        """Test getting sessions for a movie"""
        response = api_client.get(f'/api/movies/{movie.id}/sessions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1


@pytest.mark.django_db
class TestHallViewSet:
    """Test Hall API endpoints"""
    
    def test_list_halls(self, api_client, hall):
        """Test listing halls"""
        response = api_client.get('/api/halls/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_hall_detail(self, api_client, hall):
        """Test retrieving hall detail with seats"""
        response = api_client.get(f'/api/halls/{hall.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Hall 1'
        assert 'seats' in response.data
        assert len(response.data['seats']) == 150  # 10 rows * 15 seats


@pytest.mark.django_db
class TestSessionViewSet:
    """Test Session API endpoints"""
    
    def test_list_sessions(self, api_client, session):
        """Test listing sessions"""
        response = api_client.get('/api/sessions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_session_detail(self, api_client, session):
        """Test retrieving session detail"""
        response = api_client.get(f'/api/sessions/{session.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['movie_title'] == 'Test Movie'
        assert response.data['hall_name'] == 'Hall 1'


@pytest.mark.django_db
class TestBookingViewSet:
    """Test Booking API endpoints"""
    
    def test_create_booking_authenticated(self, authenticated_client, session, hall):
        """Test creating a booking when authenticated"""
        seat = hall.seats.first()
        data = {
            'session': session.id,
            'seat': seat.id
        }
        response = authenticated_client.post('/api/bookings/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Booking.objects.filter(user__email='test@example.com').exists()
    
    def test_create_booking_not_authenticated(self, api_client, session, hall):
        """Test creating booking without authentication fails"""
        seat = hall.seats.first()
        data = {
            'session': session.id,
            'seat': seat.id
        }
        response = api_client.post('/api/bookings/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_double_booking_prevention(self, authenticated_client, session, hall):
        """Test that double booking is prevented"""
        seat = hall.seats.first()
        data = {
            'session': session.id,
            'seat': seat.id
        }
        # First booking should succeed
        response1 = authenticated_client.post('/api/bookings/', data, format='json')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Second booking of same seat should fail
        response2 = authenticated_client.post('/api/bookings/', data, format='json')
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_user_bookings(self, authenticated_client, booking):
        """Test listing user's bookings"""
        response = authenticated_client.get('/api/bookings/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_booking_detail(self, authenticated_client, booking):
        """Test retrieving booking detail"""
        response = authenticated_client.get(f'/api/bookings/{booking.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'pending'
    
    def test_cancel_booking(self, authenticated_client, booking):
        """Test cancelling a booking"""
        data = {'status': 'cancelled'}
        response = authenticated_client.patch(f'/api/bookings/{booking.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        booking.refresh_from_db()
        assert booking.status == 'cancelled'
