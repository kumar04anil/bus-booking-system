import React, { useState, useEffect } from 'react';
import { searchAPI } from '../api/client';
import '../styles/SearchForm.css';

export default function SearchForm({ onSearch }) {
  const [cities, setCities] = useState([]);
  const [formData, setFormData] = useState({
    source: '',
    destination: '',
    journey_date: new Date().toISOString().split('T')[0],
    passenger_count: 1,
    bus_type: '',
    ac_type: '',
    journey_window: ''
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    searchAPI.getCities()
      .then(res => {
        setCities(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching cities:', err);
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.source || !formData.destination) {
      alert('Please select source and destination');
      return;
    }
    onSearch(formData);
  };

  const swapCities = () => {
    setFormData(prev => ({
      ...prev,
      source: prev.destination,
      destination: prev.source
    }));
  };

  if (loading) return <div className="search-form"><p>Loading cities...</p></div>;

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <h1>🚌 Bus Booking System</h1>
      
      <div className="search-container">
        <div className="form-group">
          <label>From</label>
          <select name="source" value={formData.source} onChange={handleChange} required>
            <option value="">Select City</option>
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        <button type="button" className="swap-btn" onClick={swapCities}>⇄</button>

        <div className="form-group">
          <label>To</label>
          <select name="destination" value={formData.destination} onChange={handleChange} required>
            <option value="">Select City</option>
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Date</label>
          <input 
            type="date" 
            name="journey_date" 
            value={formData.journey_date} 
            onChange={handleChange}
            min={new Date().toISOString().split('T')[0]}
            required 
          />
        </div>

        <div className="form-group">
          <label>Passengers</label>
          <input 
            type="number" 
            name="passenger_count" 
            value={formData.passenger_count} 
            onChange={handleChange}
            min="1" 
            max="6"
            required 
          />
        </div>
      </div>

      <div className="filters-container">
        <div className="form-group">
          <label>Bus Type</label>
          <select name="bus_type" value={formData.bus_type} onChange={handleChange}>
            <option value="">Any</option>
            <option value="sleeper">Sleeper</option>
            <option value="chair">Chair Car</option>
          </select>
        </div>

        <div className="form-group">
          <label>AC Type</label>
          <select name="ac_type" value={formData.ac_type} onChange={handleChange}>
            <option value="">Any</option>
            <option value="AC">AC</option>
            <option value="Non-AC">Non-AC</option>
          </select>
        </div>

        <div className="form-group">
          <label>Journey</label>
          <select name="journey_window" value={formData.journey_window} onChange={handleChange}>
            <option value="">Any Time</option>
            <option value="day">Day</option>
            <option value="night">Night</option>
          </select>
        </div>
      </div>

      <button type="submit" className="search-btn">Search Buses</button>
    </form>
  );
}
