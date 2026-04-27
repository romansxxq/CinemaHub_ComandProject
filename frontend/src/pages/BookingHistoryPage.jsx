import { useState, useEffect } from 'react';
import { bookingService } from '../services/api';
import '../styles/BookingHistoryPage.css';

function BookingHistoryPage() {
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
      const response = await bookingService.getHistory();
      
      let filteredBookings = response.data;
      if (filterStatus !== 'all') {
        filteredBookings = filteredBookings.filter(b => b.status === filterStatus);
      }
      
      setBookings(filteredBookings);
      setError(null);
    } catch (err) {
      setError('Failed to load booking history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return;
    }

    try {
      await bookingService.cancel(bookingId);
      loadBookings();
      alert('Booking cancelled successfully');
    } catch (err) {
      alert('Failed to cancel booking');
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
        return '✓ Paid';
      case 'pending':
        return '⏳ Pending Payment';
      case 'cancelled':
        return '✗ Cancelled';
      default:
        return status;
    }
  };

  return (
    <div className="booking-history-page">
      <div className="history-container">
        <div className="history-header">
          <h1>📋 Booking History</h1>

          <div className="filter-buttons">
            <button
              className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
              onClick={() => setFilterStatus('all')}
            >
              All Bookings
            </button>
            <button
              className={`filter-btn ${filterStatus === 'paid' ? 'active' : ''}`}
              onClick={() => setFilterStatus('paid')}
            >
              Paid
            </button>
            <button
              className={`filter-btn ${filterStatus === 'pending' ? 'active' : ''}`}
              onClick={() => setFilterStatus('pending')}
            >
              Pending
            </button>
            <button
              className={`filter-btn ${filterStatus === 'cancelled' ? 'active' : ''}`}
              onClick={() => setFilterStatus('cancelled')}
            >
              Cancelled
            </button>
          </div>
        </div>

        {loading && <div className="loading">Loading bookings...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && bookings.length === 0 && (
          <div className="no-bookings">
            No bookings found for the selected filter.
          </div>
        )}

        {!loading && bookings.length > 0 && (
          <div className="bookings-table">
            <table>
              <thead>
                <tr>
                  <th>Movie</th>
                  <th>Date & Time</th>
                  <th>Hall</th>
                  <th>Seat</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {bookings.map((booking) => (
                  <tr key={booking.id}>
                    <td className="movie-name">
                      <strong>{booking.movie_title}</strong>
                    </td>
                    <td className="datetime">
                      {new Date(booking.session_time).toLocaleDateString()}
                      <br />
                      {new Date(booking.session_time).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false,
                      })}
                    </td>
                    <td>{booking.hall_name}</td>
                    <td>{booking.seat_info}</td>
                    <td className="price">₴{parseFloat(booking.price).toFixed(2)}</td>
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
                          Cancel
                        </button>
                      )}
                      {booking.status !== 'cancelled' && (
                        <span className="ticket-id" title="Ticket ID">
                          {booking.id}
                        </span>
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
