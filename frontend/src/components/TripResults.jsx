import React from 'react';
import '../styles/TripResults.css';

export default function TripResults({ results, onSelectTrip, loading, error }) {
  if (loading) {
    return <div className="trips-container"><p className="loading">Searching buses...</p></div>;
  }

  if (error) {
    return <div className="trips-container"><p className="error">Error: {error}</p></div>;
  }

  if (!results || results.length === 0) {
    return <div className="trips-container"><p className="no-results">No buses found. Try different filters.</p></div>;
  }

  const sortResults = (trips, sortBy) => {
    const sorted = [...trips];
    switch(sortBy) {
      case 'price':
        return sorted.sort((a, b) => a.fare.total - b.fare.total);
      case 'rating':
        return sorted.sort((a, b) => (b.driver?.rating || 0) - (a.driver?.rating || 0));
      case 'departure':
        return sorted.sort((a, b) => a.departure_time.localeCompare(b.departure_time));
      default:
        return sorted;
    }
  };

  const displayResults = sortResults(results, 'price');

  return (
    <div className="trips-container">
      <h2>Available Buses ({results.length})</h2>
      
      <div className="trips-list">
        {displayResults.map(trip => (
          <div key={trip.trip_id} className="trip-card">
            <div className="trip-header">
              <div className="bus-info">
                <h3>{trip.bus.name}</h3>
                <p className="bus-details">
                  {trip.bus.type.toUpperCase()} • {trip.bus.ac_type} • {trip.bus.total_seats} seats
                </p>
                <p className="amenities">
                  {trip.bus.amenities.join(' • ')}
                </p>
              </div>

              <div className="route-info">
                <div className="time-section">
                  <p className="departure-time">{trip.departure_time}</p>
                  <p className="route-label">{trip.route.source.substring(0, 3).toUpperCase()}</p>
                </div>
                <div className="duration-section">
                  <p className="duration">~12h</p>
                  <p className="arrow">→</p>
                </div>
                <div className="time-section">
                  <p className="arrival-time">{trip.arrival_time}</p>
                  <p className="route-label">{trip.route.destination.substring(0, 3).toUpperCase()}</p>
                </div>
              </div>
            </div>

            <div className="trip-details">
              {trip.driver && (
                <div className="driver-info">
                  <p><strong>Driver:</strong> {trip.driver.name}</p>
                  <p><strong>Rating:</strong> ⭐ {trip.driver.rating} ({trip.driver.experience_years}y exp)</p>
                </div>
              )}

              <div className="availability">
                <p>
                  <strong>Seats:</strong> {trip.availability.available_seats}/{trip.availability.total_seats} available
                </p>
              </div>
            </div>

            <div className="trip-footer">
              <div className="fare-section">
                <div className="fare-breakdown">
                  <p className="base-fare">₹{trip.fare.base_fare}</p>
                  <p className="small-text">Base: ₹{trip.fare.base_fare}</p>
                  <p className="small-text">GST: ₹{trip.fare.gst}</p>
                  <p className="small-text">Conv: ₹{trip.fare.convenience_fee}</p>
                </div>
                <div className="total-section">
                  <p className="total-fare">₹{trip.fare.total}</p>
                  <p className="small-text">per person</p>
                </div>
              </div>

              <button 
                className="select-btn"
                onClick={() => onSelectTrip(trip)}
              >
                Select Bus
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
