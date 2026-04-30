import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { movieService } from '../services/api';
import { SkeletonMovieDetail } from '../components/Skeleton';
import { ErrorState, EmptySessions } from '../components/EmptyState';
import { useToast } from '../context/ToastContext';
import '../styles/MovieDetailPage.css';

function MovieDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const [movie, setMovie] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);

  useEffect(() => {
    loadMovieAndSessions();
  }, [id]);

  const loadMovieAndSessions = async () => {
    try {
      setLoading(true);
      setError(null);
      const movieRes = await movieService.getById(id);
      setMovie(movieRes.data);

      const sessionsRes = await movieService.getSessions(id);
      const sessionsList = sessionsRes.data.results || sessionsRes.data;
      
      setSessions(sessionsList);
      
      if (sessionsList.length > 0) {
        const firstDate = new Date(sessionsList[0].start_time).toDateString();
        setSelectedDate(firstDate);
      }
    } catch (err) {
      const message = err.response?.data?.detail || 'Не вдалося завантажити деталі фільму';
      setError(message);
      toast.error(message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSessionsByDate = () => {
    if (!selectedDate) return [];
    
    return sessions.filter((session) => {
      const sessionDate = new Date(session.start_time).toDateString();
      return sessionDate === selectedDate;
    });
  };

  const getUniqueDates = () => {
    const dates = new Set();
    sessions.forEach((session) => {
      dates.add(new Date(session.start_time).toDateString());
    });
    return Array.from(dates).sort();
  };

  const formatTime = (dateTime) => {
    return new Date(dateTime).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    });
  };

  const handleSessionClick = (sessionId) => {
    navigate(`/seat-selection/${sessionId}`);
  };

  if (loading) return <SkeletonMovieDetail />;
  if (error) return <ErrorState message={error} />;
  if (!movie) return <ErrorState message="Фільм не знайдено" />;

  const sessionsByDate = getSessionsByDate();
  const uniqueDates = getUniqueDates();

  return (
    <div className="movie-detail-page">
      <div className="movie-banner" style={{
        backgroundImage: `url(${movie.poster_url})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}>
        <div className="banner-overlay"></div>
      </div>

      <div className="movie-container">
        <div className="movie-header">
          <div className="movie-poster">
            <img 
              src={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image'}
              alt={movie.title}
              onError={(e) => { e.target.src = 'https://via.placeholder.com/300x450?text=No+Image'; }}
            />
          </div>

          <div className="movie-info">
            <h1>{movie.title}</h1>
            <div className="movie-meta">
              <span className="rating-badge">{movie.rating}</span>
              <span className="duration">⏱️ {movie.duration} minutes</span>
            </div>

            {movie.release_date && (
              <p className="release-date">
                📅 Released: {new Date(movie.release_date).toLocaleDateString()}
              </p>
            )}

            <div className="movie-details">
              {movie.director && (
                <p><strong>Director:</strong> {movie.director}</p>
              )}
              {movie.actors && (
                <p><strong>Cast:</strong> {movie.actors}</p>
              )}
            </div>

            <div className="description">
              <h3>Synopsis</h3>
              <p>{movie.description}</p>
            </div>

            {movie.genres && movie.genres.length > 0 && (
              <div className="genres">
                <strong>Genres:</strong>
                {movie.genres.map((genre) => (
                  <span key={genre.id} className="genre-tag">{genre.name}</span>
                ))}
              </div>
            )}
          </div>
        </div>

        {movie.trailer_url && (
          <div className="trailer-section">
            <h2>Trailer</h2>
            <div className="trailer-container">
              <iframe
                width="100%"
                height="500"
                src={movie.trailer_url}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title="Movie Trailer"
              ></iframe>
            </div>
          </div>
        )}

        <div className="sessions-section">
          <h2>Виберіть сеанс</h2>

          <div className="date-selector">
            <h3>Виберіть дату:</h3>
            <div className="dates-list">
              {uniqueDates.map((date) => (
                <button
                  key={date}
                  className={`date-btn ${selectedDate === date ? 'active' : ''}`}
                  onClick={() => setSelectedDate(date)}
                >
                  {new Date(date).toLocaleDateString('uk-UA', {
                    weekday: 'short',
                    month: 'short',
                    day: 'numeric',
                  })}
                </button>
              ))}
            </div>
          </div>

          {sessionsByDate.length > 0 ? (
            <div className="sessions-list">
              <h3>Доступні сеанси:</h3>
              <div className="sessions-grid">
                {sessionsByDate.map((session) => (
                  <div key={session.id} className="session-card">
                    <div className="session-time">
                      {formatTime(session.start_time)}
                    </div>
                    <div className="session-type">
                      {session.hall_type_name}
                    </div>
                    <div className="session-hall">
                      Зал: {session.hall_name}
                    </div>
                    <div className="session-price">
                      <span className="price-label">Звичайне:</span>
                      <span className="price-value">₴{session.base_price_standard}</span>
                    </div>
                    <div className="session-price">
                      <span className="price-label">VIP:</span>
                      <span className="price-value">₴{session.base_price_vip}</span>
                    </div>
                    <button
                      className="book-btn"
                      onClick={() => handleSessionClick(session.id)}
                    >
                      Забронювати місця →
                    </button>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <EmptySessions />
          )}
        </div>
      </div>
    </div>
  );
}

export default MovieDetailPage;
