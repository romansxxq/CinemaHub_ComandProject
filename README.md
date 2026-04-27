# CinemaHub - Cinema Booking System

A full-stack web application for booking cinema tickets with a Django backend and React frontend.

## Features

### 🎬 Movie Catalog
- Browse all available movies
- Search movies by name
- Filter by genre
- View now showing movies
- Detailed movie information with trailers

### 🎫 Ticket Booking
- Interactive theater seat selection
- Real-time seat availability
- Support for standard and VIP seats
- Dynamic pricing based on seat type

### 👤 User Management
- User registration and login
- JWT authentication
- User profile management
- Booking history and active bookings
- Ticket management with QR codes

### 🎭 Admin Features
- Django Admin panel for all models
- Movie management with OMDb API integration
- Theater and session management
- Booking monitoring

## Project Structure

```
CinemaHub_ComandProject/
├── backend/
│   ├── api/
│   │   ├── migrations/
│   │   ├── models.py           # Database models
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   ├── admin.py            # Django admin
│   ├── config/
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # URL configuration
│   ├── manage.py
│   ├── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── MovieCard.jsx
│   │   │   ├── SeatMap.jsx
│   │   ├── context/
│   │   │   ├── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── MovieDetailPage.jsx
│   │   │   ├── SeatSelectionPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── ProfilePage.jsx
│   │   │   ├── BookingHistoryPage.jsx
│   │   ├── services/
│   │   │   ├── api.js          # API client
│   │   ├── styles/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   ├── package.json
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create environment file (.env):**
```bash
# backend/.env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser (admin):**
```bash
python manage.py createsuperuser
```

7. **Start backend server:**
```bash
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file (.env.local):**
```bash
# frontend/.env.local
VITE_API_URL=http://localhost:8000/api
```

4. **Start development server:**
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update user profile

### Movies
- `GET /api/movies/` - List all movies
- `GET /api/movies/{id}/` - Get movie details
- `GET /api/movies/now_showing/` - Get movies currently showing
- `GET /api/movies/by_genre/?genre_id=` - Get movies by genre
- `GET /api/movies/{id}/sessions/` - Get sessions for a movie

### Genres
- `GET /api/genres/` - List all genres

### Sessions
- `GET /api/sessions/` - List all sessions
- `GET /api/sessions/{id}/` - Get session details
- `GET /api/sessions/upcoming_sessions/` - Get upcoming sessions

### Bookings
- `GET /api/bookings/` - List user bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get booking details
- `GET /api/bookings/active/` - Get active bookings
- `GET /api/bookings/history/` - Get booking history
- `POST /api/bookings/{id}/cancel/` - Cancel booking
- `POST /api/bookings/{id}/mark_paid/` - Mark as paid

## Database Models

### User
- Custom user model with email authentication
- Email as unique identifier

### Movie
- Title, description, poster, trailer URL
- Duration, rating (G, PG, PG-13, R, NC-17)
- Genres, director, actors
- Release date, "now showing" status

### Genre
- Name of movie genre

### Hall
- Hall name, number of rows, seats per row

### Seat
- Belongs to hall
- Row and seat number
- Seat type (standard/VIP)

### HallType
- Hall format (2D, 3D, IMAX)

### Session
- Movie, hall, hall type
- Start time, pricing for standard and VIP seats

### Booking
- User booking for a seat in a session
- Status (pending, paid, cancelled)
- UUID for ticket identification

## Technologies Used

### Backend
- Django 5.2
- Django REST Framework
- Django CORS Headers
- JWT Authentication (SimpleJWT)
- SQLite

### Frontend
- React 19
- Vite
- React Router
- Axios
- CSS3

## Future Enhancements

- Payment gateway integration (Stripe, PayPal)
- Email notifications
- QR code generation and validation
- Advanced filtering and sorting
- User reviews and ratings
- Wishlist feature
- Group booking discounts
- Mobile responsiveness improvements
- Dark mode
- Multi-language support

## Troubleshooting

### CORS Issues
Make sure `CORS_ALLOWED_ORIGINS` in Django settings includes your frontend URL.

### Token Expiration
The access token expires after 1 hour. Refresh token is automatically used when needed.

### Database Issues
If you encounter migration issues, try:
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for learning purposes.

## Support

For issues and questions, please open an issue in the repository.
