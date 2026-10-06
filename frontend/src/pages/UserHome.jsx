import React, { useState, useEffect } from 'react';
import { ShieldAlert, User, Calendar, Stethoscope, AlertTriangle, ArrowRight } from 'lucide-react';
import LocationPicker from '../components/LocationPicker';
import { getCurrentLocation } from '../services/location';
import { dispatchEmergency } from '../services/api';

export default function UserHome({ setDispatchResult, setActiveTab }) {
  const [patientName, setPatientName] = useState('');
  const [age, setAge] = useState('');
  const [emergencyType, setEmergencyType] = useState('Chest Pain');
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Auto-detect browser location on mount
  useEffect(() => {
    getCurrentLocation().then((loc) => setLocation(loc));
  }, []);

  const handleSubmitEmergency = async (e) => {
    e.preventDefault();
    if (!patientName.trim()) {
      setErrorMsg("Please enter Patient Name.");
      return;
    }
    if (!age || isNaN(age) || parseInt(age) <= 0) {
      setErrorMsg("Please enter a valid Patient Age.");
      return;
    }
    if (!location) {
      setErrorMsg("Acquiring current location... Please wait or click 'Detect Location'.");
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const payload = {
        patient_name: patientName.trim(),
        age: parseInt(age),
        emergency_type: emergencyType,
        latitude: location.latitude,
        longitude: location.longitude,
        phone: "9876543210"
      };

      const res = await dispatchEmergency(payload);
      setDispatchResult(res.data);
      setActiveTab('emergency-status');
    } catch (err) {
      console.error("Emergency Dispatch Error:", err);
      const detail = err.response?.data?.detail || "Failed to dispatch ambulance. Please check backend server.";
      setErrorMsg(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '750px', margin: '0 auto' }}>
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
          <ShieldAlert size={32} color="#ef4444" />
          <div>
            <h2 style={{ fontSize: '1.5rem', color: '#f8fafc', fontWeight: '700' }}>Report Medical Emergency</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
              Automated Smart Ambulance Dispatch & Hospital Selection System
            </p>
          </div>
        </div>

        {errorMsg && (
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: '8px', padding: '0.85rem 1rem', margin: '1rem 0', color: '#fca5a5', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={18} />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmitEmergency} style={{ marginTop: '1.25rem' }}>
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <User size={16} /> Patient Name
              </label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Rahul Kumar"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <Calendar size={16} /> Age
              </label>
              <input
                type="number"
                className="form-input"
                placeholder="e.g. 34"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Stethoscope size={16} /> Emergency Type
            </label>
            <select
              className="form-select"
              value={emergencyType}
              onChange={(e) => setEmergencyType(e.target.value)}
            >
              <option value="Chest Pain">Chest Pain (High Priority)</option>
              <option value="Breathing Problem">Breathing Problem (High Priority)</option>
              <option value="Accident / Injury">Accident / Injury (High Priority)</option>
              <option value="Other">Other (Normal Priority)</option>
            </select>
          </div>

          <div style={{ margin: '1.25rem 0' }}>
            <LocationPicker location={location} setLocation={setLocation} />
          </div>

          <button
            type="submit"
            className="btn btn-danger"
            disabled={loading}
            style={{ width: '100%', padding: '1rem', fontSize: '1.1rem', marginTop: '0.5rem' }}
          >
            {loading ? (
              <span>Running Dijkstra & Priority Queue Dispatch...</span>
            ) : (
              <>
                <ShieldAlert size={22} />
                <span>REQUEST AMBULANCE</span>
                <ArrowRight size={20} />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
