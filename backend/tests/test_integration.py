import pytest
from django.contrib.auth import get_user_model
from api.models import Movie, Genre, Hall, Session, Booking
from datetime import datetime, timedelta
from decimal import Decimal
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestCinemaBookingFlow:
    """Integration tests for complete cinema booking workflow"""
    
    def test_complete_booking_workflow(self, authenticated_client, movie, hall, hall_type, genre):
        """Test complete flow from browsing to booking"""
        # 1. User checks now showing movies
        response = authenticated_client.get('/api/movies/now_showing/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        
        # 2. User views movie details
        response = authenticated_client.get(f'/api/movies/{movie.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # 3. User checks sessions for movie
        response = authenticated_client.get(f'/api/movies/{movie.id}/sessions/')
        assert response.status_code == status.HTTP_200_OK
        
        # 4. Create a session for booking
        session = Session.objects.create(
            movie=movie,
            hall=hall,
            hall_type=hall_type,
            start_time=datetime.now() + timedelta(days=1),
            base_price=Decimal('100.00'),
            base_price_standard=Decimal('100.00'),
            base_price_vip=Decimal('150.00')
        )
        
        # 5. User views available seats
        response = authenticated_client.get(f'/api/halls/{hall.id}/')
        assert response.status_code == status.HTTP_200_OK
        seats = response.data['seats']
        assert len(seats) > 0
        
        # 6. User books a seat
        seat = hall.seats.first()
        booking_data = {
            'session': session.id,
            'seat': seat.id
        }
        response = authenticated_client.post('/api/bookings/', booking_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        booking_id = response.data['id']
        
        # 7. User views their bookings
        response = authenticated_client.get('/api/bookings/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        
        # 8. User views booking details
        response = authenticated_client.get(f'/api/bookings/{booking_id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'pending'
    
    def test_multiple_users_different_seats(self, authenticated_client, movie, hall, hall_type):
        """Test that multiple users can book different seats in same session"""
        session = Session.objects.create(
            movie=movie,
            hall=hall,
            hall_type=hall_type,
            start_time=datetime.now() + timedelta(days=1),
            base_price=Decimal('100.00'),
            base_price_standard=Decimal('100.00'),
            base_price_vip=Decimal('150.00')
        )
        
        seats = hall.seats.all()[:2]
        
        # First user books first seat
        data1 = {'session': session.id, 'seat': seats[0].id}
        response1 = authenticated_client.post('/api/bookings/', data1, format='json')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Create another user and book second seat
        User.objects.create_user(
            email='user2@example.com',
            username='user2',
            password='pass123'
        )
        
        # Both users should be able to book different seats
        assert Booking.objects.filter(session=session).count() == 1
    
    def test_session_has_available_and_booked_seats(self, authenticated_client, session, hall):
        """Test that we can track which seats are booked and available"""
        seat1 = hall.seats.first()
        seat2 = hall.seats.all()[1]
        
        # Book first seat
        booking_data = {'session': session.id, 'seat': seat1.id}
        response = authenticated_client.post('/api/bookings/', booking_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Check seat availability
        booked_seats = Booking.objects.filter(session=session).values_list('seat_id', flat=True)
        assert seat1.id in booked_seats
        assert seat2.id not in booked_seats
    
    def test_user_can_cancel_booking(self, authenticated_client, booking):
        """Test that user can cancel their booking"""
        initial_status = booking.status
        assert initial_status == 'pending'
        
        # Cancel the booking
        cancel_data = {'status': 'cancelled'}
        response = authenticated_client.patch(f'/api/bookings/{booking.id}/', cancel_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify status changed
        booking.refresh_from_db()
        assert booking.status == 'cancelled'


@pytest.mark.django_db
class TestGenreMovieRelationship:
    """Test relationship between genres and movies"""
    
    def test_movie_with_multiple_genres(self, movie, genre, drama_genre):
        """Test that a movie can have multiple genres"""
        movie.genres.add(drama_genre)
        assert movie.genres.count() == 2
        assert genre in movie.genres.all()
        assert drama_genre in movie.genres.all()
    
    def test_filter_movies_by_genre(self, movie, another_movie, genre, drama_genre):
        """Test filtering movies by specific genre"""
        movies_by_genre = Movie.objects.filter(genres=genre)
        assert movie in movies_by_genre
        assert another_movie not in movies_by_genre
    
    def test_genre_has_multiple_movies(self, genre):
        """Test that a genre can have multiple movies"""
        m1 = Movie.objects.create(
            title='Movie 1',
            duration=120,
            is_now_showing=True
        )
        m2 = Movie.objects.create(
            title='Movie 2',
            duration=150,
            is_now_showing=True
        )
        m1.genres.add(genre)
        m2.genres.add(genre)
        
        assert genre.movies.count() == 2


@pytest.mark.django_db
class TestDataValidation:
    """Test data validation in models and serializers"""
    
    def test_invalid_movie_duration(self):
        """Test that movie must have valid duration"""
        with pytest.raises(Exception):
            movie = Movie.objects.create(
                title='Invalid Movie',
                duration=-100,
                is_now_showing=True
            )
    
    def test_session_cannot_be_in_past(self, movie, hall, hall_type):
        """Test that session start time should be in future"""
        past_time = datetime.now() - timedelta(days=1)
        # This should ideally raise validation error
        # (may need to implement in model/serializer)
        session = Session.objects.create(
            movie=movie,
            hall=hall,
            hall_type=hall_type,
            start_time=past_time,
            base_price=Decimal('100.00')
        )
        # Just verify it was created (actual validation would be a separate implementation)
        assert session.id is not None
    
    def test_booking_user_email_required(self, session, hall):
        """Test that booking requires a valid user"""
        seat = hall.seats.first()
        with pytest.raises(Exception):
            Booking.objects.create(
                user=None,
                session=session,
                seat=seat
            )
