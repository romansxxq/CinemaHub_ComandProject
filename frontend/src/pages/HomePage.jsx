import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import MovieCard from '../components/MovieCard';
import { SkeletonGrid } from '../components/Skeleton';
import { EmptyMovies } from '../components/EmptyState';
import { movieService, genreService } from '../services/api';
import { useToast } from '../context/ToastContext';
import '../styles/HomePage.css';

function HomePage() {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedGenre, setSelectedGenre] = useState(null);
  const [showNowOnly, setShowNowOnly] = useState(false);
  const [searchParams] = useSearchParams();
  const toast = useToast();

  const searchQuery = searchParams.get('search');

  useEffect(() => {
    loadMovies();
    loadGenres();
  }, [selectedGenre, showNowOnly, searchQuery]);

  const loadMovies = async () => {
    try {
      setLoading(true);
      setError(null);
      let response;

      if (selectedGenre) {
        response = await movieService.getByGenre(selectedGenre);
      } else if (showNowOnly) {
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

  const loadGenres = async () => {
    try {
      const response = await genreService.getAll();
      setGenres(response.data.results || response.data);
    } catch (err) {
      console.error('Failed to load genres:', err);
    }
  };

  const handleGenreSelect = (genreId) => {
    setSelectedGenre(selectedGenre === genreId ? null : genreId);
    setShowNowOnly(false);
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
              setSelectedGenre(null);
            }}
          >
            📽️ Now Showing
          </button>
        </div>

        <div className="genres-scroll">
          <h3>Genres:</h3>
          <div className="genres-list">
            {genres.map((genre) => (
              <button
                key={genre.id}
                className={`genre-btn ${selectedGenre === genre.id ? 'active' : ''}`}
                onClick={() => handleGenreSelect(genre.id)}
              >
                {genre.name}
              </button>
            ))}
          </div>
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
            <h2>{showNowOnly ? 'Зараз у прокаті' : selectedGenre ? 'Фільми за жанром' : searchQuery ? 'Результати пошуку' : 'Всі фільми'}</h2>
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
