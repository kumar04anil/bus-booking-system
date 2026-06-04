import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Search endpoints
export const searchAPI = {
  getCities: () => api.get('/search/cities'),
  searchTrips: (params) => api.get('/search/trips', { params }),
};

// Booking endpoints
export const bookingAPI = {
  getSeatMap: (tripId, fromStop, toStop) => 
    api.get(`/booking/seats/${tripId}`, { params: { from_stop: fromStop, to_stop: toStop } }),
  lockSeats: (tripId, seatNumbers) => 
    api.post('/booking/lock', { trip_id: tripId, seat_numbers: seatNumbers }),
  releaseSeats: (tripId, seatNumbers) => 
    api.post('/booking/release', { trip_id: tripId, seat_numbers: seatNumbers }),
  confirmBooking: (bookingData) => 
    api.post('/booking/confirm', bookingData),
  getBooking: (bookingId) => 
    api.get(`/booking/${bookingId}`),
  getBookingByPNR: (pnr) => 
    api.get(`/booking/pnr/${pnr}`),
  cancelBooking: (bookingId) => 
    api.post(`/booking/cancel/${bookingId}`),
  getUserBookings: (userId) => 
    api.get(`/booking/user/${userId}`),
  getRefundEstimate: (bookingId) => 
    api.get(`/booking/refund/${bookingId}`),
};

export default api;
