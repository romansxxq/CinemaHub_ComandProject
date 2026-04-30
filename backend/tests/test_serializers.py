import pytest
from django.contrib.auth import get_user_model
from api.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    GenreSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    SessionSerializer,
    BookingListSerializer
)
from api.models import Movie, Genre

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializer:
    """Test User serializer"""
    
    def test_serialize_user(self, authenticated_user):
        """Test user serialization"""
        serializer = UserSerializer(authenticated_user)
        data = serializer.data
        assert data['email'] == 'test@example.com'
        assert data['username'] == 'testuser'
        assert 'id' in data
    
    def test_user_serializer_fields(self, authenticated_user):
        """Test that serializer includes correct fields"""
        serializer = UserSerializer(authenticated_user)
        assert 'id' in serializer.data
        assert 'email' in serializer.data
        assert 'username' in serializer.data
        assert 'first_name' in serializer.data


@pytest.mark.django_db
class TestUserRegisterSerializer:
    """Test User registration serializer"""
    
    def test_register_user_valid(self):
        """Test user registration with valid data"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'newuser@example.com'
        assert user.check_password('securepass123')
    
    def test_register_user_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = {
            'email': 'user@example.com',
            'username': 'user',
            'password': 'password123',
            'password_confirm': 'different123',
            'first_name': 'Jane'
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
    def test_register_user_short_password(self):
        """Test registration with password too short"""
        data = {
            'email': 'user@example.com',
            'username': 'user',
            'password': 'short',
            'password_confirm': 'short',
            'first_name': 'Test'
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestGenreSerializer:
    """Test Genre serializer"""
    
    def test_serialize_genre(self, genre):
        """Test genre serialization"""
        serializer = GenreSerializer(genre)
        assert serializer.data['name'] == 'Action'
        assert 'id' in serializer.data
    
    def test_serialize_multiple_genres(self):
        """Test serializing multiple genres"""
        Genre.objects.create(name='Comedy')
        Genre.objects.create(name='Horror')
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        assert len(serializer.data) == 2


@pytest.mark.django_db
class TestMovieSerializer:
    """Test Movie serializers"""
    
    def test_movie_list_serializer(self, movie):
        """Test movie list serializer"""
        serializer = MovieListSerializer(movie)
        data = serializer.data
        assert data['title'] == 'Test Movie'
        assert data['duration'] == 120
        assert 'id' in data
    
    def test_movie_list_serializer_includes_genres(self, movie, genre):
        """Test that movie list serializer includes genres"""
        serializer = MovieListSerializer(movie)
        data = serializer.data
        assert 'genres' in data
        assert len(data['genres']) == 1
        assert data['genres'][0]['name'] == 'Action'
    
    def test_movie_detail_serializer(self, movie):
        """Test movie detail serializer"""
        serializer = MovieDetailSerializer(movie)
        data = serializer.data
        assert data['title'] == 'Test Movie'
        assert data['description'] == 'A great test movie'
        assert data['poster_url'] == 'https://example.com/poster.jpg'
    
    def test_movie_detail_serializer_all_fields(self, movie):
        """Test that detail serializer includes all fields"""
        serializer = MovieDetailSerializer(movie)
        data = serializer.data
        expected_fields = ['id', 'title', 'description', 'poster_url', 'duration']
        for field in expected_fields:
            assert field in data


@pytest.mark.django_db
class TestSessionSerializer:
    """Test Session serializer"""
    
    def test_session_serializer(self, session):
        """Test session serialization"""
        serializer = SessionSerializer(session)
        data = serializer.data
        assert data['movie'] == session.movie.id
        assert data['hall'] == session.hall.id
        assert 'start_time' in data
    
    def test_session_serializer_computed_fields(self, session):
        """Test session serializer computed fields"""
        serializer = SessionSerializer(session)
        data = serializer.data
        assert data['movie_title'] == 'Test Movie'
        assert data['hall_name'] == 'Hall 1'
        assert 'end_time' in data
    
    def test_session_serializer_prices(self, session):
        """Test session serializer price fields"""
        serializer = SessionSerializer(session)
        data = serializer.data
        assert str(data['base_price_standard']) == '100.00'
        assert str(data['base_price_vip']) == '150.00'


@pytest.mark.django_db
class TestBookingSerializer:
    """Test Booking serializer"""
    
    def test_booking_list_serializer(self, booking):
        """Test booking list serializer"""
        serializer = BookingListSerializer(booking)
        data = serializer.data
        assert 'id' in data
        assert data['status'] == 'pending'
        assert 'user' in data
