import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { bookingService } from '../services/api';
import '../styles/ProfilePage.css';

function ProfilePage() {
  const { user, loadUser } = useAuth();
  const [activeBookings, setActiveBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadActiveBookings();
  }, []);

  const loadActiveBookings = async () => {
    try {
      setLoading(true);
      const response = await bookingService.getActive();
      setActiveBookings(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load bookings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    await loadUser();
    await loadActiveBookings();
  };

  if (!user) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <h1>👤 My Profile</h1>
          <button className="refresh-btn" onClick={handleRefresh}>
            🔄 Refresh
          </button>
        </div>

        <div className="profile-card">
          <h2>Account Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Email</label>
              <p>{user.email}</p>
            </div>
            <div className="info-item">
              <label>Username</label>
              <p>{user.username}</p>
            </div>
            <div className="info-item">
              <label>First Name</label>
              <p>{user.first_name || 'Not set'}</p>
            </div>
            <div className="info-item">
              <label>Last Name</label>
              <p>{user.last_name || 'Not set'}</p>
            </div>
          </div>
        </div>

        <div className="active-bookings">
          <h2>🎬 Active Bookings</h2>
          
          {loading && <div className="loading">Loading...</div>}
          {error && <div className="error">{error}</div>}
          
          {!loading && activeBookings.length === 0 && (
            <p className="no-bookings">You have no active bookings.</p>
          )}

          {!loading && activeBookings.length > 0 && (
            <div className="bookings-list">
              {activeBookings.map((booking) => (
                <div key={booking.id} className="booking-item">
                  <div className="booking-details">
                    <div className="booking-title">
                      <h3>{booking.movie_title}</h3>
                      <span className={`status-badge ${booking.status}`}>
                        {booking.status === 'paid' ? '✓ Paid' : '⏳ Pending'}
                      </span>
                    </div>
                    <p className="booking-datetime">
                      📅 {new Date(booking.session_time).toLocaleDateString()}
                      &nbsp;⏰ {new Date(booking.session_time).toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit',
                        hour12: false 
                      })}
                    </p>
                    <p className="booking-hall">
                      🎭 {booking.hall_name} | {booking.seat_info}
                    </p>
                    <p className="booking-price">
                      💰 ₴{parseFloat(booking.price).toFixed(2)}
                    </p>
                  </div>
                  <div className="booking-actions">
                    <div className="ticket-id">
                      Ticket ID: {booking.id}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
