import React, { useState } from 'react';
import { searchAPI } from './api/client';
import SearchForm from './components/SearchForm';
import TripResults from './components/TripResults';
import SeatSelection from './components/SeatSelection';
import BookingConfirmation from './components/BookingConfirmation';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('search'); // search, results, seats, booking
  const [searchParams, setSearchParams] = useState(null);
  const [tripResults, setTripResults] = useState([]);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchError, setSearchError] = useState(null);

  const handleSearch = async (params) => {
    setLoading(true);
    setSearchError(null);
    try {
      const res = await searchAPI.searchTrips(params);
      setTripResults(res.data.results || []);
      setSearchParams(params);
      setCurrentPage('results');
    } catch (err) {
      setSearchError(err.message);
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTrip = (trip) => {
    setSelectedTrip(trip);
    setCurrentPage('seats');
  };

  const handleSeatsSelected = (seats) => {
    setSelectedSeats(seats);
    setCurrentPage('booking');
  };

  const handleBackFromSeats = () => {
    setCurrentPage('results');
    setSelectedSeats([]);
  };

  const handleBackFromBooking = () => {
    setCurrentPage('seats');
  };

  const handleBackToSearch = () => {
    setCurrentPage('search');
    setTripResults([]);
    setSelectedTrip(null);
    setSelectedSeats([]);
    setSearchError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚌 Bus Booking System</h1>
        {currentPage !== 'search' && (
          <button className="home-btn" onClick={handleBackToSearch}>← New Search</button>
        )}
      </header>

      <main className="app-main">
        {currentPage === 'search' && (
          <SearchForm onSearch={handleSearch} />
        )}

        {currentPage === 'results' && (
          <TripResults
            results={tripResults}
            onSelectTrip={handleSelectTrip}
            loading={loading}
            error={searchError}
          />
        )}

        {currentPage === 'seats' && selectedTrip && (
          <SeatSelection
            trip={selectedTrip}
            fromStop={searchParams.source}
            toStop={searchParams.destination}
            onProceed={handleSeatsSelected}
            onBack={handleBackFromSeats}
          />
        )}

        {currentPage === 'booking' && selectedTrip && (
          <BookingConfirmation
            trip={selectedTrip}
            selectedSeats={selectedSeats}
            fromStop={searchParams.source}
            toStop={searchParams.destination}
            onBack={handleBackFromBooking}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>© 2026 Bus Booking System | API Documentation: <a href="/docs">/docs</a></p>
      </footer>
    </div>
  );
}

export default App;
