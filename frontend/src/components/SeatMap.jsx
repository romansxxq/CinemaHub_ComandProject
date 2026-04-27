import { useState } from 'react';
import '../styles/SeatMap.css';

function SeatMap({ seats, bookedSeats = [], selectedSeats = {}, onSeatSelect = () => {} }) {
  const [hoveredSeat, setHoveredSeat] = useState(null);

  if (!seats || seats.length === 0) {
    return <div className="empty-seats">No seats available</div>;
  }

  // Group seats by row
  const seatsByRow = {};
  seats.forEach((seat) => {
    if (!seatsByRow[seat.row]) {
      seatsByRow[seat.row] = [];
    }
    seatsByRow[seat.row].push(seat);
  });

  const rows = Object.keys(seatsByRow).sort((a, b) => parseInt(a) - parseInt(b));

  return (
    <div className="seat-map">
      <div className="screen">🎬 SCREEN</div>
      
      <div className="seats-container">
        {rows.map((rowNum) => (
          <div key={rowNum} className="seat-row">
            <div className="row-label">Row {rowNum}</div>
            <div className="row-seats">
              {seatsByRow[rowNum]
                .sort((a, b) => a.number - b.number)
                .map((seat) => {
                  const isBooked = bookedSeats.includes(seat.id);
                  const isSelected = selectedSeats[seat.id];
                  const isHovered = hoveredSeat?.id === seat.id;

                  return (
                    <button
                      key={seat.id}
                      className={`seat ${seat.seat_type} ${isBooked ? 'booked' : ''} ${isSelected ? 'selected' : ''} ${isHovered ? 'hovered' : ''}`}
                      disabled={isBooked}
                      onClick={() => onSeatSelect(seat)}
                      onMouseEnter={() => !isBooked && setHoveredSeat(seat)}
                      onMouseLeave={() => setHoveredSeat(null)}
                      title={isBooked ? 'Seat occupied' : `Row ${seat.row}, Seat ${seat.number}`}
                    >
                      {isHovered && !isBooked && (
                        <div className="seat-tooltip">
                          Row {seat.row}, Seat {seat.number}
                        </div>
                      )}
                    </button>
                  );
                })}
            </div>
            <div className="row-label">Row {rowNum}</div>
          </div>
        ))}
      </div>

      <div className="seat-legend">
        <div className="legend-item">
          <div className="legend-seat available"></div>
          <span>Available</span>
        </div>
        <div className="legend-item">
          <div className="legend-seat vip"></div>
          <span>VIP</span>
        </div>
        <div className="legend-item">
          <div className="legend-seat booked"></div>
          <span>Occupied</span>
        </div>
        <div className="legend-item">
          <div className="legend-seat selected"></div>
          <span>Selected</span>
        </div>
      </div>
    </div>
  );
}

export default SeatMap;
