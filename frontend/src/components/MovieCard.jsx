import { Link } from 'react-router-dom';
import '../styles/MovieCard.css';

function MovieCard({ movie }) {
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
          {movie.genres && movie.genres.slice(0, 2).map((genre) => (
            <span key={genre.id} className="genre-tag">{genre.name}</span>
          ))}
        </div>
        <button className="buy-ticket-btn">Buy Ticket →</button>
      </div>
    </Link>
  );
}

export default MovieCard;
