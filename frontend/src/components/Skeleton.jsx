import '../styles/Skeleton.css';

export function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-image"></div>
      <div className="skeleton-body">
        <div className="skeleton skeleton-title"></div>
        <div className="skeleton skeleton-text"></div>
        <div className="skeleton skeleton-text" style={{ width: '80%' }}></div>
        <div className="skeleton skeleton-button"></div>
      </div>
    </div>
  );
}

export function SkeletonMovieDetail() {
  return (
    <div className="skeleton-movie-detail">
      <div className="skeleton skeleton-banner"></div>
      <div className="skeleton-header">
        <div className="skeleton skeleton-poster"></div>
        <div className="skeleton-info">
          <div className="skeleton skeleton-title" style={{ width: '60%' }}></div>
          <div className="skeleton skeleton-text"></div>
          <div className="skeleton skeleton-text"></div>
          <div className="skeleton skeleton-text" style={{ width: '70%' }}></div>
        </div>
      </div>
    </div>
  );
}

export function SkeletonSeatMap() {
  return (
    <div className="skeleton-seat-map">
      <div className="skeleton skeleton-screen"></div>
      <div className="skeleton skeleton-seats"></div>
    </div>
  );
}

export function SkeletonGrid() {
  return (
    <div className="skeleton-grid">
      {[...Array(8)].map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
