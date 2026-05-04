"""
Initial data setup script for CinemaHub
Run with: python manage.py shell < setup_data.py
"""

from api.models import Movie, Hall, HallType, Seat, Session
from django.utils import timezone
from datetime import datetime, timedelta

# Create HallTypes
print("\nCreating hall types...")
hall_types_data = ['2D', '3D', 'IMAX']
hall_types = {}
for hall_type_name in hall_types_data:
    hall_type, created = HallType.objects.get_or_create(name=hall_type_name)
    hall_types[hall_type_name] = hall_type
    if created:
        print(f"  ✓ Created hall type: {hall_type_name}")

# Create Halls
print("\nCreating halls...")
halls_data = [
    {'name': 'Hall 1', 'rows': 10, 'seats_per_row': 15},
    {'name': 'Hall 2', 'rows': 12, 'seats_per_row': 20},
    {'name': 'Hall 3', 'rows': 8, 'seats_per_row': 16},
]
halls = {}
for hall_data in halls_data:
    hall, created = Hall.objects.get_or_create(
        name=hall_data['name'],
        defaults={'rows': hall_data['rows'], 'seats_per_row': hall_data['seats_per_row']}
    )
    halls[hall_data['name']] = hall
    if created:
        print(f"  ✓ Created hall: {hall_data['name']}")
        
        # Create seats for this hall
        for row in range(1, hall_data['rows'] + 1):
            for seat_num in range(1, hall_data['seats_per_row'] + 1):
                # Make last few rows VIP
                is_vip = row >= hall_data['rows'] - 2
                Seat.objects.get_or_create(
                    hall=hall,
                    row=row,
                    number=seat_num,
                    defaults={'seat_type': 'vip' if is_vip else 'standard'}
                )
        print(f"    Created {hall_data['rows'] * hall_data['seats_per_row']} seats")

# Create Sample Movies
print("\nCreating sample movies...")
movies_data = [
    {
        'title': 'The Matrix Reloaded',
        'description': 'Neo and his allies race against time before the machines discover the city of Zion and destroy it.',
        'duration': 138,
        'rating': 'R',
        'genres': ['Action', 'Sci-Fi'],
        'director': 'Lana Wachowski, Lilly Wachowski',
        'actors': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
        'release_date': datetime(2003, 5, 15).date(),
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2EzM2FmNDUtYWE0OS00YWQ1LTkzYzItMzc2MjJiN2M1ZmU5XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
        'trailer_url': 'https://www.youtube.com/embed/4S9SntjIWUg',
    },
    {
        'title': 'Inception',
        'description': 'A skilled thief who steals corporate secrets through the use of dream-sharing technology.',
        'duration': 148,
        'rating': 'PG-13',
        'genres': ['Action', 'Sci-Fi', 'Thriller'],
        'director': 'Christopher Nolan',
        'actors': 'Leonardo DiCaprio, Marion Cotillard, Ellen Page',
        'release_date': datetime(2010, 7, 16).date(),
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjAxMzc5ZDctNTkxOC00ZDRhLTg4YjUtRWM0N2FjNTA0NzA1XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_.jpg',
        'trailer_url': 'https://www.youtube.com/embed/YoHD_XwzAv4',
    },
    {
        'title': 'Inside Out',
        'description': 'After moving to a new city, a young girl is helped by her emotions.',
        'duration': 98,
        'rating': 'PG',
        'genres': ['Animation', 'Comedy', 'Drama'],
        'director': 'Pete Docter',
        'actors': 'Amy Poehler, Phyllis Smith, Richard Kind',
        'release_date': datetime(2015, 6, 19).date(),
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BOTc1NjU0NjAwM15BMl5BanBnXkFtZTgwMDg4Nzc1MDE@._V1_.jpg',
        'trailer_url': 'https://www.youtube.com/embed/yRUAzGQ3nSY',
    },
    {
        'title': 'Doctor Strange',
        'description': 'A neurosurgeon discovers the mystic arts.',
        'duration': 115,
        'rating': 'PG-13',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'director': 'Scott Derrickson',
        'actors': 'Benedict Cumberbatch, Chiwetel Ejiofor, Rachel McAdams',
        'release_date': datetime(2016, 11, 4).date(),
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjgwNzAc3NzcyOF5BMl5BanBnXkFtZTgwMzc2MTI1OTE@._V1_.jpg',
        'trailer_url': 'https://www.youtube.com/embed/HSzx-zc9Mk8',
    },
]

movies = {}
for movie_data in movies_data:
    genres_list = movie_data.pop('genres')

    # Genres are stored as plain text on Movie
    movie_data['genres_text'] = ', '.join(genres_list)
    movie, created = Movie.objects.get_or_create(
        title=movie_data['title'],
        defaults=movie_data
    )
    movies[movie_data['title']] = movie
    
    if created:
        print(f"  ✓ Created movie: {movie_data['title']}")

# Create Sessions
print("\nCreating sessions...")
now = timezone.now()
session_times = [
    now + timedelta(hours=2),
    now + timedelta(hours=5),
    now + timedelta(hours=8),
    now + timedelta(days=1, hours=2),
    now + timedelta(days=1, hours=5),
]

for movie_title, movie in movies.items():
    for idx, time in enumerate(session_times):
        hall_key = f"Hall {(idx % 3) + 1}"
        hall = halls[hall_key]
        hall_type = hall_types[['2D', '3D', 'IMAX'][idx % 3]]
        
        session, created = Session.objects.get_or_create(
            movie=movie,
            hall=hall,
            start_time=time,
            defaults={
                'hall_type': hall_type,
                'base_price_standard': 100,
                'base_price_vip': 150,
            }
        )
        if created:
            print(f"  ✓ Created session: {movie_title} - {time.strftime('%Y-%m-%d %H:%M')}")

print("\n✅ Initial data setup complete!")
