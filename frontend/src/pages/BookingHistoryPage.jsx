import { useState, useEffect } from 'react';
import { bookingService } from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { EmptyBookings } from '../components/EmptyState';
import '../styles/BookingHistoryPage.css';

function BookingHistoryPage() {
  const toast = useToast();
  const { user } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    loadBookings();
  }, [filterStatus]);

  const loadBookings = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await bookingService.getHistory();
      
      let filteredBookings = response.data;
      if (filterStatus !== 'all') {
        filteredBookings = filteredBookings.filter(b => b.status === filterStatus);
      }
      
      setBookings(filteredBookings);
    } catch (err) {
      const message = err.response?.data?.detail || 'Не вдалося завантажити історію бронювань';
      setError(message);
      toast.error(message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Ви впевнені, що хочете скасувати це бронювання?')) {
      return;
    }

    try {
      await bookingService.cancel(bookingId);
      toast.success('Бронювання скасовано');
      loadBookings();
    } catch (err) {
      const message = err.response?.data?.error
        || err.response?.data?.detail
        || 'Не вдалося скасувати бронювання';
      toast.error(message);
      console.error(err);
    }
  };

  const handleDownloadTicket = async (bookingId) => {
    try {
      const response = await bookingService.downloadTicketReport(bookingId);
      const url = URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = url;
      link.download = `ticket-${bookingId}.pdf`;
      link.click();
      URL.revokeObjectURL(url);
      toast.success('Електронний квиток завантажено');
    } catch (err) {
      toast.error('Не вдалося сформувати електронний квиток');
      console.error(err);
    }
  };

  const handleDownloadFinancialReport = async () => {
    try {
      const response = await bookingService.downloadFinancialReport({});
      const url = URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'financial-analytics.xlsx';
      link.click();
      URL.revokeObjectURL(url);
      toast.success('Фінансовий звіт завантажено');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Не вдалося сформувати фінансовий звіт');
      console.error(err);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid':
        return 'status-paid';
      case 'pending':
        return 'status-pending';
      case 'cancelled':
        return 'status-cancelled';
      default:
        return '';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'paid':
        return '✓ Оплачено';
      case 'pending':
        return '⏳ Заброньовано';
      case 'cancelled':
        return '✗ Скасовано';
      default:
        return status;
    }
  };

  return (
    <div className="booking-history-page">
      <div className="history-container">
        <div className="history-header">
          <h1>📋 Історія бронювань</h1>

          <div className="filter-buttons">
            <button
              className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
              onClick={() => setFilterStatus('all')}
            >
              Всі бронювання
            </button>
            <button
              className={`filter-btn ${filterStatus === 'paid' ? 'active' : ''}`}
              onClick={() => setFilterStatus('paid')}
            >
              Оплачені
            </button>
            <button
              className={`filter-btn ${filterStatus === 'pending' ? 'active' : ''}`}
              onClick={() => setFilterStatus('pending')}
            >
              Заброньовані
            </button>
            <button
              className={`filter-btn ${filterStatus === 'cancelled' ? 'active' : ''}`}
              onClick={() => setFilterStatus('cancelled')}
            >
              Скасовані
            </button>
            {user?.is_staff && (
              <button className="report-btn financial-report-btn" onClick={handleDownloadFinancialReport}>
                Фінансовий звіт
              </button>
            )}
          </div>
        </div>

        {loading && <div className="loading">Загрузка бронювань...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && bookings.length === 0 && (
          <EmptyBookings />
        )}

        {!loading && bookings.length > 0 && (
          <div className="bookings-table">
            <table>
              <thead>
                <tr>
                  <th>Фільм</th>
                  <th>Дата та час</th>
                  <th>Зал</th>
                  <th>Місце</th>
                  <th>Ціна</th>
                  <th>Статус</th>
                  <th>Дії</th>
                </tr>
              </thead>
              <tbody>
                {bookings.map((booking) => (
                  <tr key={booking.id}>
                    <td className="movie-name">
                      <strong>{booking.movie_title}</strong>
                    </td>
                    <td className="datetime">
                      {new Date(booking.session_time).toLocaleDateString('uk-UA')}
                      <br />
                      {new Date(booking.session_time).toLocaleTimeString('uk-UA', {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false,
                      })}
                    </td>
                    <td>{booking.hall_name}</td>
                    <td>{booking.seat_info}</td>
                    <td className="price">
                      {Number.isFinite(Number(booking.price))
                        ? `₴${Number(booking.price).toFixed(2)}`
                        : 'Ціну не вказано'}
                    </td>
                    <td>
                      <span className={`status-badge ${getStatusColor(booking.status)}`}>
                        {getStatusLabel(booking.status)}
                      </span>
                    </td>
                    <td className="actions">
                      {booking.status === 'pending' && (
                        <button
                          className="cancel-btn"
                          onClick={() => handleCancelBooking(booking.id)}
                        >
                          Скасувати
                        </button>
                      )}
                      {booking.status !== 'cancelled' && (
                        <>
                          <button
                            className="report-btn"
                            onClick={() => handleDownloadTicket(booking.id)}
                          >
                            PDF-квиток
                          </button>
                          <span className="ticket-id" title="ID білету">{booking.id}</span>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default BookingHistoryPage;
