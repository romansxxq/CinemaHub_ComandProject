import { Link } from 'react-router-dom';
import '../styles/MovieCard.css';

function MovieCard({ movie }) {
  const genreNames = (() => {
    if (!movie?.genres) return [];
    if (Array.isArray(movie.genres)) {
      return movie.genres.map((g) => g?.name).filter(Boolean);
    }
    if (typeof movie.genres === 'string') {
      return movie.genres.split(',').map((g) => g.trim()).filter(Boolean);
    }
    return [];
  })();

  return (
    <Link to={`/movie/${movie.id}`} className="movie-card">
      <div className="card-image">
        <img 
          src={movie.poster_url || 'https://via.placeholder.com/200x300?text=No+Image'} 
          alt={movie.title}
          onError={(e) => { e.target.src = 'https://via.placeholder.com/200x300?text=No+Image'; }}
        />
      </div>
      <div className="card-body">
        <h3 className="card-title">{movie.title}</h3>
        <div className="card-info">
          <span className="rating-badge">{movie.rating}</span>
          <span className="duration">{movie.duration} min</span>
        </div>
        <div className="card-genres">
          {genreNames.slice(0, 2).map((name) => (
            <span key={name} className="genre-tag">{name}</span>
          ))}
        </div>
        <button className="buy-ticket-btn">Buy Ticket →</button>
      </div>
    </Link>
  );
}

export default MovieCard;
