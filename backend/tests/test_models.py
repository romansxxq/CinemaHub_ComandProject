import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model functionality"""
    
    def test_create_user(self):
        """Test creating a new user"""
        user = User.objects.create_user(
            email='newuser@example.com',
            username='newuser',
            password='testpass123'
        )
        assert user.email == 'newuser@example.com'
        assert user.username == 'newuser'
        assert user.check_password('testpass123')
    
    def test_user_email_unique(self):
        """Test that email must be unique"""
        User.objects.create_user(
            email='duplicate@example.com',
            username='user1',
            password='pass123'
        )
        with pytest.raises(Exception):
            User.objects.create_user(
                email='duplicate@example.com',
                username='user2',
                password='pass123'
            )
    
    def test_user_str_representation(self, authenticated_user):
        """Test user string representation returns email"""
        assert str(authenticated_user) == 'test@example.com'
    
    def test_user_password_hashing(self):
        """Test that passwords are properly hashed"""
        user = User.objects.create_user(
            email='hash@example.com',
            username='hashuser',
            password='password123'
        )
        assert user.password != 'password123'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')


@pytest.mark.django_db
class TestGenreModel:
    """Test Genre model functionality"""
    
    def test_create_genre(self, genre):
        """Test creating a genre"""
        assert genre.name == 'Action'
        assert str(genre) == 'Action'
    
    def test_genre_unique_name(self, genre):
        """Test that genre names must be unique"""
        from api.models import Genre
        with pytest.raises(Exception):
            Genre.objects.create(name='Action')


@pytest.mark.django_db
class TestMovieModel:
    """Test Movie model functionality"""
    
    def test_create_movie(self, movie):
        """Test creating a movie"""
        assert movie.title == 'Test Movie'
        assert movie.duration == 120
        assert movie.is_now_showing is True
    
    def test_movie_with_genres(self, movie, genre):
        """Test movie has correct genres"""
        assert genre in movie.genres.all()
    
    def test_movie_string_representation(self, movie):
        """Test movie string representation"""
        assert str(movie) == 'Test Movie'
    
    def test_movie_now_showing_filter(self, movie, another_movie):
        """Test filtering movies by now_showing status"""
        from api.models import Movie
        now_showing = Movie.objects.filter(is_now_showing=True)
        assert movie in now_showing
        assert another_movie not in now_showing


@pytest.mark.django_db
class TestHallModel:
    """Test Hall model functionality"""
    
    def test_create_hall(self, hall):
        """Test creating a hall"""
        assert hall.name == 'Hall 1'
        assert hall.rows == 10
        assert hall.seats_per_row == 15
    
    def test_hall_auto_creates_seats(self, hall):
        """Test that hall creation auto-generates seats"""
        total_seats = hall.seats.count()
        expected_seats = hall.rows * hall.seats_per_row
        assert total_seats == expected_seats
    
    def test_hall_vip_seats_last_row(self, hall):
        """Test that last row seats are marked as VIP"""
        vip_seats = hall.seats.filter(row=hall.rows, is_vip=True)
        assert vip_seats.count() == hall.seats_per_row
    
    def test_hall_standard_seats_not_vip(self, hall):
        """Test that non-last row seats are not VIP"""
        standard_seats = hall.seats.filter(row=1, is_vip=False)
        assert standard_seats.count() == hall.seats_per_row
    
    def test_seat_unique_constraint(self, hall):
        """Test that seat combination must be unique"""
        from api.models import Seat
        first_seat = hall.seats.first()
        with pytest.raises(Exception):
            Seat.objects.create(
                hall=hall,
                row=first_seat.row,
                number=first_seat.number,
                is_vip=False
            )


@pytest.mark.django_db
class TestSessionModel:
    """Test Session model functionality"""
    
    def test_create_session(self, session):
        """Test creating a session"""
        assert session.movie.title == 'Test Movie'
        assert session.hall.name == 'Hall 1'
        assert str(session.base_price) == '100.00'
    
    def test_session_end_time_calculation(self, session):
        """Test that end_time is calculated from duration"""
        from datetime import timedelta
        expected_end = session.start_time + timedelta(minutes=120)
        assert session.end_time == expected_end
    
    def test_session_string_representation(self, session):
        """Test session string representation"""
        assert 'Test Movie' in str(session)


@pytest.mark.django_db
class TestBookingModel:
    """Test Booking model functionality"""
    
    def test_create_booking(self, booking):
        """Test creating a booking"""
        assert booking.user.email == 'test@example.com'
        assert booking.status == 'pending'
    
    def test_booking_status_choices(self, booking):
        """Test booking has valid status"""
        valid_statuses = ['pending', 'paid', 'cancelled']
        assert booking.status in valid_statuses
    
    def test_booking_unique_session_seat(self, booking, session, hall):
        """Test that one seat can't be booked twice in same session"""
        from api.models import Booking
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        another_user = User.objects.create_user(
            email='another@example.com',
            username='another',
            password='pass123'
        )
        
        with pytest.raises(Exception):
            Booking.objects.create(
                user=another_user,
                session=session,
                seat=booking.seat,
                status='pending'
            )
    
    def test_booking_has_uuid_id(self, booking):
        """Test that booking has UUID as ID"""
        import uuid
        assert isinstance(booking.id, uuid.UUID)
    
    def test_booking_string_representation(self, booking):
        """Test booking string representation"""
        assert 'Ticket' in str(booking)
        assert 'test@example.com' in str(booking)
