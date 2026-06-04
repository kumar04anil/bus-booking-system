import React, { useState } from 'react';
import { bookingAPI } from '../api/client';
import '../styles/BookingConfirmation.css';

export default function BookingConfirmation({ trip, selectedSeats, fromStop, toStop, onBack }) {
  const [passengers, setPassengers] = useState(
    selectedSeats.map((seat, idx) => ({
      seat_number: seat,
      name: '',
      age: '',
      gender: 'male',
      contact: '',
      special_requests: ''
    }))
  );
  const [paymentMethod, setPaymentMethod] = useState('UPI');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bookingResult, setBookingResult] = useState(null);

  const handlePassengerChange = (idx, field, value) => {
    const updated = [...passengers];
    updated[idx][field] = value;
    setPassengers(updated);
  };

  const calculateTotal = () => {
    const baseTotal = trip.fare.base_fare * selectedSeats.length;
    const gst = baseTotal * 0.18;
    return baseTotal + gst + trip.fare.convenience_fee;
  };

  const handleConfirmBooking = async () => {
    // Validation
    const allFieldsFilled = passengers.every(p => p.name && p.age && p.contact);
    if (!allFieldsFilled) {
      setError('Please fill all passenger details');
      return;
    }

    setLoading(true);
    try {
      const bookingData = {
        trip_id: trip.trip_id,
        user_id: 'u1', // Mock user
        from_stop: fromStop,
        to_stop: toStop,
        passengers,
        payment_method: paymentMethod
      };

      const res = await bookingAPI.confirmBooking(bookingData);
      setBookingResult(res.data);
      setError(null);
    } catch (err) {
      setError('Booking failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (bookingResult) {
    return (
      <div className="booking-confirmation">
        <div className="confirmation-success">
          <h2>✅ Booking Confirmed!</h2>
          <div className="pnr-box">
            <p className="pnr-label">PNR:</p>
            <p className="pnr-number">{bookingResult.pnr}</p>
          </div>

          <div className="booking-summary">
            <h3>Booking Details</h3>
            <p><strong>Trip:</strong> {trip.bus.name} ({trip.bus.number})</p>
            <p><strong>Route:</strong> {fromStop} → {toStop}</p>
            <p><strong>Seats:</strong> {selectedSeats.join(', ')}</p>
            <p><strong>Passengers:</strong> {passengers.map(p => p.name).join(', ')}</p>
            <p><strong>Total Amount:</strong> ₹{bookingResult.total_amount}</p>
          </div>

          <button 
            className="new-booking-btn"
            onClick={() => window.location.href = '/'}
          >
            Make Another Booking
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="booking-confirmation">
      <div className="confirmation-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h2>Passenger Details & Payment</h2>
      </div>

      <div className="confirmation-content">
        <div className="trip-summary">
          <h3>Trip Summary</h3>
          <p><strong>{trip.bus.name}</strong> - {trip.bus.number}</p>
          <p>{trip.departure_time} from {trip.route.source}</p>
          <p>{trip.arrival_time} to {trip.route.destination}</p>
          <p>Seats: <strong>{selectedSeats.join(', ')}</strong></p>
        </div>

        <div className="passengers-form">
          <h3>Passenger Details</h3>
          {passengers.map((passenger, idx) => (
            <div key={idx} className="passenger-card">
              <h4>Seat {passenger.seat_number}</h4>
              
              <div className="form-group">
                <label>Name *</label>
                <input
                  type="text"
                  value={passenger.name}
                  onChange={(e) => handlePassengerChange(idx, 'name', e.target.value)}
                  placeholder="Full Name"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Age *</label>
                  <input
                    type="number"
                    value={passenger.age}
                    onChange={(e) => handlePassengerChange(idx, 'age', e.target.value)}
                    placeholder="Age"
                    min="1"
                  />
                </div>
                <div className="form-group">
                  <label>Gender</label>
                  <select value={passenger.gender} onChange={(e) => handlePassengerChange(idx, 'gender', e.target.value)}>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Contact *</label>
                <input
                  type="tel"
                  value={passenger.contact}
                  onChange={(e) => handlePassengerChange(idx, 'contact', e.target.value)}
                  placeholder="Phone Number"
                />
              </div>

              <div className="form-group">
                <label>Special Requests</label>
                <input
                  type="text"
                  value={passenger.special_requests}
                  onChange={(e) => handlePassengerChange(idx, 'special_requests', e.target.value)}
                  placeholder="Any special requests"
                />
              </div>
            </div>
          ))}
        </div>

        <div className="payment-section">
          <h3>Payment Method</h3>
          <div className="payment-options">
            {['UPI', 'Card', 'Net Banking'].map(method => (
              <label key={method} className="payment-option">
                <input
                  type="radio"
                  value={method}
                  checked={paymentMethod === method}
                  onChange={(e) => setPaymentMethod(e.target.value)}
                />
                <span>{method}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="fare-summary">
          <h3>Fare Breakdown</h3>
          <div className="fare-row">
            <span>Base Fare:</span>
            <span>₹{trip.fare.base_fare} × {selectedSeats.length}</span>
          </div>
          <div className="fare-row">
            <span>GST (18%):</span>
            <span>₹{(trip.fare.base_fare * selectedSeats.length * 0.18).toFixed(2)}</span>
          </div>
          <div className="fare-row">
            <span>Convenience Fee:</span>
            <span>₹{trip.fare.convenience_fee}</span>
          </div>
          <div className="fare-row total">
            <span>Total:</span>
            <span>₹{calculateTotal()}</span>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button 
          className="confirm-btn"
          onClick={handleConfirmBooking}
          disabled={loading}
        >
          {loading ? 'Processing...' : '✓ Confirm Booking'}
        </button>
      </div>
    </div>
  );
}
