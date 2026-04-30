import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from decimal import Decimal
from api.models import Genre, Movie, Hall, Seat, Session, HallType, Booking

User = get_user_model()


@pytest.fixture
def api_client():
    """Create an API client instance"""
    return APIClient()


@pytest.fixture
def authenticated_user(db):
    """Create an authenticated user"""
    user = User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )
    return user


@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    """Create an authenticated API client"""
    api_client.force_authenticate(user=authenticated_user)
    return api_client


@pytest.fixture
def genre(db):
    """Create a test genre"""
    return Genre.objects.create(name='Action')


@pytest.fixture
def drama_genre(db):
    """Create another test genre"""
    return Genre.objects.create(name='Drama')


@pytest.fixture
def movie(db, genre):
    """Create a test movie"""
    movie = Movie.objects.create(
        title='Test Movie',
        description='A great test movie',
        poster_url='https://example.com/poster.jpg',
        trailer_url='https://example.com/trailer.mp4',
        duration=120,
        is_now_showing=True,
        release_date=datetime.now().date()
    )
    movie.genres.add(genre)
    return movie


@pytest.fixture
def another_movie(db, drama_genre):
    """Create another test movie"""
    movie = Movie.objects.create(
        title='Drama Movie',
        description='A dramatic movie',
        poster_url='https://example.com/poster2.jpg',
        trailer_url='https://example.com/trailer2.mp4',
        duration=150,
        is_now_showing=False,
        release_date=(datetime.now() - timedelta(days=30)).date()
    )
    movie.genres.add(drama_genre)
    return movie


@pytest.fixture
def hall_type(db):
    """Create a test hall type"""
    return HallType.objects.create(name='Standard')


@pytest.fixture
def hall(db):
    """Create a test hall with seats"""
    hall = Hall.objects.create(
        name='Hall 1',
        rows=10,
        seats_per_row=15
    )
    return hall


@pytest.fixture
def session(db, movie, hall, hall_type):
    """Create a test session"""
    start_time = datetime.now() + timedelta(days=1)
    return Session.objects.create(
        movie=movie,
        hall=hall,
        hall_type=hall_type,
        start_time=start_time,
        base_price=Decimal('100.00'),
        base_price_standard=Decimal('100.00'),
        base_price_vip=Decimal('150.00')
    )


@pytest.fixture
def booking(db, authenticated_user, session, hall):
    """Create a test booking"""
    seat = hall.seats.first()
    return Booking.objects.create(
        user=authenticated_user,
        session=session,
        seat=seat,
        status='pending'
    )


@pytest.fixture
def db(db):
    """Override db fixture to ensure database is clean"""
    return db
