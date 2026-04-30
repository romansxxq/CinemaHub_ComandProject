import '../styles/Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>🎬 CinemaHub</h3>
          <p>Ваш персональний кінотеатр. Бронюйте квитки онлайн і насолоджуйтесь фільмами.</p>
        </div>

        <div className="footer-section">
          <h4>Навігація</h4>
          <ul>
            <li><a href="/">Головна</a></li>
            <li><a href="/#now-showing">Зараз у прокаті</a></li>
            <li><a href="/#genres">Жанри</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Користувачу</h4>
          <ul>
            <li><a href="/login">Вхід</a></li>
            <li><a href="/register">Реєстрація</a></li>
            <li><a href="/bookings">Мої бронювання</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Контакти</h4>
          <ul>
            <li><a href="mailto:info@cinemahub.com">info@cinemahub.com</a></li>
            <li><a href="tel:+380961234567">+38 (096) 123-45-67</a></li>
            <li><a href="#">Написати нам</a></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; {currentYear} CinemaHub. Всі права захищені.</p>
        <div className="footer-links">
          <a href="#">Політика приватності</a>
          <span className="divider">•</span>
          <a href="#">Умови використання</a>
          <span className="divider">•</span>
          <a href="#">Допомога</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
