import '../styles/EmptyState.css';

export function EmptyMovies() {
  return (
    <div className="empty-state">
      <div className="empty-icon">🎬</div>
      <h2>Фільмів не знайдено</h2>
      <p>За вашим запитом не знайдено жодних фільмів. Спробуйте змінити фільтри або повернітеся пізніше.</p>
    </div>
  );
}

export function EmptyBookings() {
  return (
    <div className="empty-state">
      <div className="empty-icon">🎫</div>
      <h2>У вас немає бронювань</h2>
      <p>Почніть з пошуку фільму та придбайте квитки на улюблений фільм.</p>
    </div>
  );
}

export function EmptySessions() {
  return (
    <div className="empty-state">
      <div className="empty-icon">📅</div>
      <h2>На цю дату немає сеансів</h2>
      <p>Спробуйте вибрати іншу дату або повернітеся пізніше.</p>
    </div>
  );
}

export function EmptyGenres() {
  return (
    <div className="empty-state">
      <div className="empty-icon">🎭</div>
      <h2>Жанрів не знайдено</h2>
      <p>Будь ласка, спробуйте пізніше.</p>
    </div>
  );
}

export function ErrorState({ message = 'Щось пішло не так' }) {
  return (
    <div className="empty-state error-state">
      <div className="empty-icon">⚠️</div>
      <h2>Помилка</h2>
      <p>{message}</p>
    </div>
  );
}
