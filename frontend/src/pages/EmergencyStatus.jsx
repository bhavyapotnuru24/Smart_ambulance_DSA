import React, { useState } from 'react';
import { Truck, Hospital, Stethoscope, Navigation, CheckCircle2, User, Clock, Star, RefreshCw } from 'lucide-react';
import MapView from '../components/MapView';
import DsaExplanationCard from '../components/DsaExplanationCard';
import { resetAmbulanceStatus } from '../services/api';

export default function EmergencyStatus({ dispatchResult, setActiveTab, setDispatchResult }) {
  const [resetting, setResetting] = useState(false);
  const [selectedRouteIdx, setSelectedRouteIdx] = useState(0);

  if (!dispatchResult) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <h3>No active emergency dispatch found.</h3>
        <button className="btn btn-primary" onClick={() => setActiveTab('user-home')} style={{ marginTop: '1rem' }}>
          Report Emergency
        </button>
      </div>
    );
  }

  const {
    emergency_code,
    priority,
    ambulance,
    hospital,
    assigned_doctor,
    existing_patient_record,
    match_method,
    selected_route,
    alternative_routes,
    dsa_explanation
  } = dispatchResult;

  const currentRoute = alternative_routes[selectedRouteIdx] || selected_route;

  const handleCompleteEmergency = async () => {
    if (!ambulance || !ambulance.id) return;
    setResetting(true);
    try {
      await resetAmbulanceStatus(ambulance.id);
      alert(`Emergency ${emergency_code} Completed! Ambulance ${ambulance.ambulance_code} is now AVAILABLE again.`);
      setDispatchResult(null);
      setActiveTab('user-home');
    } catch (err) {
      console.error("Failed to reset ambulance:", err);
    } finally {
      setResetting(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #065f46 0%, #064e3b 100%)', borderColor: '#059669' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div className="badge badge-success" style={{ fontSize: '0.9rem', marginBottom: '0.4rem' }}>
              <CheckCircle2 size={16} /> AMBULANCE DISPATCHED
            </div>
            <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#ffffff' }}>
              Emergency Ref: {emergency_code}
            </h2>
            <div style={{ fontSize: '0.9rem', color: '#a7f3d0' }}>
              Priority Level: <strong>{priority}</strong> | Patient Record: <strong>{existing_patient_record?.name || 'Registered'}</strong> ({match_method})
            </div>
          </div>

          <button
            className="btn btn-success"
            onClick={handleCompleteEmergency}
            disabled={resetting}
            style={{ padding: '0.75rem 1.25rem' }}
          >
            <RefreshCw size={18} className={resetting ? "spin" : ""} />
            {resetting ? "Completing..." : "Complete Emergency & Free Ambulance"}
          </button>
        </div>
      </div>

      {/* Main Details Grid */}
      <div className="grid-3">
        {/* Ambulance Unit */}
        <div className="card">
          <div className="card-title" style={{ color: '#38bdf8' }}>
            <Truck size={22} /> Dispatched Ambulance
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#ffffff', margin: '0.5rem 0' }}>
            Unit {ambulance.ambulance_code}
          </div>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>
            Status: <span className="badge badge-info">{ambulance.status}</span>
          </div>
          <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: '#cbd5e1' }}>
            <div>Driver: <strong>{ambulance.driver_name || 'Ramesh Kumar'}</strong></div>
            <div>Phone: <strong>{ambulance.driver_phone || '9849012345'}</strong></div>
          </div>
        </div>

        {/* Selected Hospital */}
        <div className="card">
          <div className="card-title" style={{ color: '#ef4444' }}>
            <Hospital size={22} /> Target Hospital
          </div>
          <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#ffffff', margin: '0.5rem 0' }}>
            {hospital.hospital_name}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
            {hospital.address}
          </div>
          <div style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: '#cbd5e1' }}>
            Available Beds: <span className="badge badge-success">{hospital.available_beds} Beds Available</span>
          </div>
        </div>

        {/* Assigned Doctor & ETA */}
        <div className="card">
          <div className="card-title" style={{ color: '#10b981' }}>
            <Stethoscope size={22} /> Assigned Specialist
          </div>
          <div style={{ fontSize: '1.1rem', fontWeight: '700', color: '#ffffff', margin: '0.5rem 0' }}>
            {assigned_doctor ? assigned_doctor.name : "On-call Emergency Specialist"}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
            Specialization: <strong>{assigned_doctor ? assigned_doctor.specialization : "General Emergency"}</strong>
          </div>
          <div style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Clock size={16} color="#f59e0b" />
            <span>ETA: <strong>{currentRoute.eta_minutes} mins</strong> ({currentRoute.distance_km} km)</span>
          </div>
        </div>
      </div>

      {/* Map & Route Options Grid */}
      <div className="grid-3" style={{ gridTemplateColumns: '1fr 2fr' }}>
        {/* Route Candidates List */}
        <div className="card">
          <div className="card-title">
            <Navigation size={20} color="#38bdf8" />
            <span>Candidate Routes (Dijkstra)</span>
          </div>
          {alternative_routes.map((r, idx) => (
            <div
              key={r.id}
              className={`route-option ${selectedRouteIdx === idx ? 'selected' : ''}`}
              onClick={() => setSelectedRouteIdx(idx)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ color: r.is_recommended ? '#38bdf8' : '#f8fafc' }}>
                  {r.name}
                </strong>
                {r.is_recommended && (
                  <span className="badge badge-info" style={{ fontSize: '0.75rem' }}>
                    <Star size={12} fill="#38bdf8" /> Recommended
                  </span>
                )}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.3rem' }}>
                Distance: {r.distance_km} km | Est. Travel Time: <strong>{r.eta_minutes} mins</strong>
              </div>
            </div>
          ))}
        </div>

        {/* Leaflet Map Visualizer */}
        <div>
          <MapView
            userLocation={{ latitude: dispatchResult.ambulance.latitude, longitude: dispatchResult.ambulance.longitude, address: "Patient Emergency Location" }}
            hospitals={[hospital]}
            ambulances={[ambulance]}
            selectedRoute={currentRoute}
            alternativeRoutes={alternative_routes}
          />
        </div>
      </div>

      {/* Structured DSA Explanation for Review 3 */}
      <DsaExplanationCard dsaData={dsa_explanation} />
    </div>
  );
}
