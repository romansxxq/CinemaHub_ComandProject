import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import MovieCard from '../components/MovieCard';
import { SkeletonGrid } from '../components/Skeleton';
import { EmptyMovies } from '../components/EmptyState';
import { movieService } from '../services/api';
import { useToast } from '../context/ToastContext';
import '../styles/HomePage.css';

function HomePage() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showNowOnly, setShowNowOnly] = useState(false);
  const [searchParams] = useSearchParams();
  const toast = useToast();

  const searchQuery = searchParams.get('search');

  useEffect(() => {
    loadMovies();
  }, [showNowOnly, searchQuery]);

  const loadMovies = async () => {
    try {
      setLoading(true);
      setError(null);
      let response;

      if (showNowOnly) {
        response = await movieService.getNowShowing();
      } else if (searchQuery) {
        response = await movieService.getAll({ search: searchQuery });
      } else {
        response = await movieService.getAll();
      }

      setMovies(response.data.results || response.data);
    } catch (err) {
      const message = err.response?.data?.detail || 'Не вдалося завантажити фільми';
      setError(message);
      toast.error(message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      <div className="hero-banner">
        <h1>🎬 Welcome to CinemaHub</h1>
        <p>Book your favorite movies and enjoy the best cinema experience</p>
      </div>

      <div className="filters-section">
        <div className="filter-group">
          <button
            className={`filter-btn ${showNowOnly ? 'active' : ''}`}
            onClick={() => {
              setShowNowOnly(!showNowOnly);
            }}
          >
            📽️ Now Showing
          </button>
        </div>

        {searchQuery && (
          <div className="search-info">
            Search results for: <strong>"{searchQuery}"</strong>
          </div>
        )}
      </div>

      <div className="movies-section">
        {loading ? (
          <SkeletonGrid />
        ) : error ? (
          <div className="error-message">⚠️ {error}</div>
        ) : movies.length === 0 ? (
          <EmptyMovies />
        ) : (
          <>
            <h2>{showNowOnly ? 'Зараз у прокаті' : searchQuery ? 'Результати пошуку' : 'Всі фільми'}</h2>
            <div className="movies-grid">
              {movies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default HomePage;
