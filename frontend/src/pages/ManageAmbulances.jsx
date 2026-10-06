import React, { useState, useEffect } from 'react';
import { Truck, RefreshCw } from 'lucide-react';
import { getAmbulances, updateAmbulanceStatus } from '../services/api';

export default function ManageAmbulances() {
  const [ambulances, setAmbulances] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAmbulances = () => {
    setLoading(true);
    getAmbulances()
      .then((res) => setAmbulances(res.data))
      .catch((err) => console.error("Failed to load ambulances:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAmbulances();
  }, []);

  const handleStatusChange = async (id, newStatus) => {
    try {
      await updateAmbulanceStatus(id, newStatus);
      fetchAmbulances();
    } catch (err) {
      console.error("Failed to update ambulance status:", err);
    }
  };

  if (loading) return <div style={{ padding: '2rem' }}>Loading Ambulance Roster...</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#f8fafc' }}>Ambulance Fleet Management (6 Predefined Units)</h2>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Monitor and update the status of the 6 predefined emergency ambulance units (A01 to A06).
        </p>
      </div>

      <div className="grid-3">
        {ambulances.map((a) => (
          <div key={a.id} className="card" style={{ borderColor: a.status === 'Available' ? '#10b981' : a.status === 'Dispatched' ? '#0284c7' : '#334155' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#f8fafc' }}>
                Unit {a.ambulance_code}
              </div>
              <span className={`badge ${a.status === 'Available' ? 'badge-success' : a.status === 'Dispatched' ? 'badge-info' : 'badge-danger'}`}>
                {a.status}
              </span>
            </div>

            <div style={{ margin: '0.75rem 0', fontSize: '0.85rem', color: '#cbd5e1' }}>
              <div>Driver: <strong>{a.driver_name || 'Unassigned'}</strong></div>
              <div>Phone: <strong>{a.driver_phone || 'N/A'}</strong></div>
              <div>Position: <strong>{a.latitude.toFixed(4)}, {a.longitude.toFixed(4)}</strong></div>
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Update Status</label>
              <select
                className="form-select"
                value={a.status}
                onChange={(e) => handleStatusChange(a.id, e.target.value)}
                style={{ fontSize: '0.85rem' }}
              >
                <option value="Available">Available</option>
                <option value="Busy">Busy</option>
                <option value="Dispatched">Dispatched</option>
              </select>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
