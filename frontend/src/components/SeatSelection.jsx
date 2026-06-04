import React, { useState, useEffect } from 'react';
import { bookingAPI } from '../api/client';
import '../styles/SeatSelection.css';

export default function SeatSelection({ trip, fromStop, toStop, onProceed, onBack }) {
  const [seatMap, setSeatMap] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lockTimer, setLockTimer] = useState(0);

  const passengerCount = trip.availability.available_seats; // simplified

  useEffect(() => {
    const fetchSeats = async () => {
      try {
        const res = await bookingAPI.getSeatMap(trip.trip_id, fromStop, toStop);
        setSeatMap(res.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    fetchSeats();
  }, [trip, fromStop, toStop]);

  const handleSeatClick = (seatNumber) => {
    if (selectedSeats.includes(seatNumber)) {
      setSelectedSeats(selectedSeats.filter(s => s !== seatNumber));
    } else if (selectedSeats.length < passengerCount) {
      setSelectedSeats([...selectedSeats, seatNumber]);
    }
  };

  const getSeatStatus = (seat) => {
    if (selectedSeats.includes(seat.seat_number)) return 'selected';
    return seat.status;
  };

  const getSeatClass = (seat) => {
    const status = getSeatStatus(seat);
    return `seat seat-${status}`;
  };

  const handleLockSeats = async () => {
    if (selectedSeats.length === 0) {
      alert('Please select at least one seat');
      return;
    }
    try {
      await bookingAPI.lockSeats(trip.trip_id, selectedSeats);
      setLockTimer(600); // 10 minutes
      alert(`${selectedSeats.length} seat(s) locked for 10 minutes`);
    } catch (err) {
      alert('Error locking seats: ' + err.message);
    }
  };

  const handleProceed = () => {
    if (selectedSeats.length === 0) {
      alert('Please select seats');
      return;
    }
    onProceed(selectedSeats);
  };

  if (loading) return <div className="seat-selection"><p>Loading seat map...</p></div>;
  if (error) return <div className="seat-selection"><p className="error">Error: {error}</p></div>;
  if (!seatMap) return <div className="seat-selection"><p>No seat data available</p></div>;

  const isSleeper = trip.bus.type === 'sleeper';

  return (
    <div className="seat-selection">
      <div className="seat-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h2>Select Seats - {trip.bus.name}</h2>
        <p>{fromStop} → {toStop}</p>
      </div>

      <div className="seat-grid-container">
        {seatMap.grid && seatMap.grid.decks && Object.entries(seatMap.grid.decks).map(([deckName, seats]) => (
          <div key={deckName} className="deck">
            <h3>{deckName}</h3>
            <div className="seats-grid">
              {seats.map(seat => (
                <button
                  key={seat.seat_number}
                  className={getSeatClass(seat)}
                  onClick={() => seat.status === 'available' && handleSeatClick(seat.seat_number)}
                  disabled={seat.status !== 'available' && !selectedSeats.includes(seat.seat_number)}
                  title={`${seat.seat_number} - ${getSeatStatus(seat)}`}
                >
                  {seat.seat_number}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="seat-legend">
        <div className="legend-item">
          <div className="seat available"></div>
          <span>Available</span>
        </div>
        <div className="legend-item">
          <div className="seat booked"></div>
          <span>Booked</span>
        </div>
        <div className="legend-item">
          <div className="seat locked"></div>
          <span>Locked</span>
        </div>
        <div className="legend-item">
          <div className="seat female_reserved"></div>
          <span>Female Reserved</span>
        </div>
        <div className="legend-item">
          <div className="seat selected"></div>
          <span>Selected</span>
        </div>
      </div>

      <div className="seat-footer">
        <div className="selected-info">
          <p>Selected: <strong>{selectedSeats.join(', ') || 'None'}</strong></p>
          <p>Seats: {selectedSeats.length} / {passengerCount}</p>
        </div>
        <div className="actions">
          <button className="lock-btn" onClick={handleLockSeats}>🔒 Lock Seats</button>
          <button 
            className="proceed-btn" 
            onClick={handleProceed}
            disabled={selectedSeats.length === 0}
          >
            Proceed to Details →
          </button>
        </div>
      </div>
    </div>
  );
}
