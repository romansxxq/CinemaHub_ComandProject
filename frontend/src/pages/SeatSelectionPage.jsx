import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { sessionService, bookingService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { SkeletonSeatMap } from '../components/Skeleton';
import { ErrorState } from '../components/EmptyState';
import SeatMap from '../components/SeatMap';
import '../styles/SeatSelectionPage.css';

function SeatSelectionPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const toast = useToast();

  const [session, setSession] = useState(null);
  const [seats, setSeats] = useState([]);
  const [bookedSeats, setBookedSeats] = useState([]);
  const [selectedSeats, setSelectedSeats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processingBooking, setProcessingBooking] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadSessionDetails();
  }, [sessionId, isAuthenticated, navigate]);

  const loadSessionDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      const sessionRes = await sessionService.getById(sessionId);
      setSession(sessionRes.data);
      setSeats(sessionRes.data.hall.seats);
      setBookedSeats(sessionRes.data.booked_seats);
    } catch (err) {
      const message = err.response?.data?.detail || 'Не вдалося завантажити деталі сеансу';
      setError(message);
      toast.error(message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSeatSelect = (seat) => {
    setSelectedSeats((prev) => {
      const newSelected = { ...prev };
      if (newSelected[seat.id]) {
        delete newSelected[seat.id];
      } else {
        newSelected[seat.id] = seat;
      }
      return newSelected;
    });
  };

  const calculateTotal = () => {
    let total = 0;
    Object.values(selectedSeats).forEach((seat) => {
      if (seat.seat_type === 'vip') {
        total += parseFloat(session.base_price_vip);
      } else {
        total += parseFloat(session.base_price_standard);
      }
    });
    return total;
  };

  const handleBooking = async () => {
    if (Object.keys(selectedSeats).length === 0) {
      toast.warning('Будь ласка, виберіть мінімум одне місце');
      return;
    }

    try {
      setProcessingBooking(true);
      const bookings = [];

      for (const seatId of Object.keys(selectedSeats)) {
        const seat = selectedSeats[seatId];
        const bookingRes = await bookingService.create({
          session: sessionId,
          seat: seat.id,
          status: 'pending',
        });
        bookings.push(bookingRes.data);
      }

      toast.success('Бронювання успішне!');
      navigate('/bookings');
    } catch (err) {
      const message = err.response?.data?.detail || 'Не вдалося створити бронювання';
      toast.error(message);
      setError(message);
      console.error(err);
    } finally {
      setProcessingBooking(false);
    }
  };

  if (loading) return <SkeletonSeatMap />;
  if (error) return <ErrorState message={error} />;
  if (!session) return <ErrorState message="Сеанс не знайдено" />;

  const selectedCount = Object.keys(selectedSeats).length;
  const totalPrice = calculateTotal();

  return (
    <div className="seat-selection-page">
      <div className="session-info">
        <h1>Select Your Seats</h1>
        <div className="info-details">
          <p><strong>{session.movie.title}</strong></p>
          <p>
            📅 {new Date(session.start_time).toLocaleDateString()}
            &nbsp; ⏰ {new Date(session.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
          </p>
          <p>🎭 Hall: {session.hall.name} | 🎬 Format: {session.hall_type.name}</p>
        </div>
      </div>

      <div className="selection-container">
        <div className="seat-selection">
          <SeatMap
            seats={seats}
            bookedSeats={bookedSeats}
            selectedSeats={selectedSeats}
            onSeatSelect={handleSeatSelect}
          />
        </div>

        <div className="booking-summary">
          <div className="summary-card">
            <h2>Booking Summary</h2>

            <div className="selected-seats">
              <h3>Selected Seats ({selectedCount})</h3>
              {selectedCount > 0 ? (
                <div className="seats-list">
                  {Object.values(selectedSeats)
                    .sort((a, b) => {
                      if (a.row === b.row) return a.number - b.number;
                      return a.row - b.row;
                    })
                    .map((seat) => (
                      <div key={seat.id} className="seat-item">
                        <span>
                          Row {seat.row}, Seat {seat.number}
                          {seat.seat_type === 'vip' && ' (VIP)'}
                        </span>
                        <span className="seat-price">
                          ₴{seat.seat_type === 'vip' 
                            ? session.base_price_vip 
                            : session.base_price_standard}
                        </span>
                      </div>
                    ))}
                </div>
              ) : (
                <p className="no-selection">No seats selected</p>
              )}
            </div>

            <div className="price-breakdown">
              <div className="price-row">
                <span>Standard Seats:</span>
                <span>
                  ₴{session.base_price_standard}
                  {Object.values(selectedSeats).filter((s) => s.seat_type === 'standard').length > 0 && (
                    ` × ${Object.values(selectedSeats).filter((s) => s.seat_type === 'standard').length}`
                  )}
                </span>
              </div>
              <div className="price-row">
                <span>VIP Seats:</span>
                <span>
                  ₴{session.base_price_vip}
                  {Object.values(selectedSeats).filter((s) => s.seat_type === 'vip').length > 0 && (
                    ` × ${Object.values(selectedSeats).filter((s) => s.seat_type === 'vip').length}`
                  )}
                </span>
              </div>
            </div>

            <div className="total-price">
              <span>Total to Pay:</span>
              <span className="price-value">₴{totalPrice.toFixed(2)}</span>
            </div>

            <button
              className="proceed-btn"
              onClick={handleBooking}
              disabled={selectedCount === 0 || processingBooking}
            >
              {processingBooking ? 'Processing...' : 'Proceed to Payment →'}
            </button>

            <button
              className="back-btn"
              onClick={() => navigate(-1)}
              disabled={processingBooking}
            >
              ← Back
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SeatSelectionPage;
