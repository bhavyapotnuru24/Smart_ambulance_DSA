import React, { useState, useEffect } from 'react';
import { Hospital, Save, Plus } from 'lucide-react';
import { getHospitals, updateHospitalBeds } from '../services/api';

export default function ManageHospitals() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [savingId, setSavingId] = useState(null);

  const fetchHospitals = () => {
    setLoading(true);
    getHospitals()
      .then((res) => setHospitals(res.data))
      .catch((err) => console.error("Failed to load hospitals:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHospitals();
  }, []);

  const handleBedChange = (id, delta) => {
    setHospitals(hospitals.map(h => {
      if (h.id === id) {
        const newBeds = Math.max(0, h.available_beds + delta);
        return { ...h, available_beds: newBeds };
      }
      return h;
    }));
  };

  const handleSaveBeds = async (id, newBeds) => {
    setSavingId(id);
    try {
      await updateHospitalBeds(id, newBeds);
      alert("Hospital bed availability updated!");
      fetchHospitals();
    } catch (err) {
      console.error("Failed to update beds:", err);
    } finally {
      setSavingId(null);
    }
  };

  if (loading) return <div style={{ padding: '2rem' }}>Loading Hospital Database...</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#f8fafc' }}>Hospital Management</h2>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Manage hospital bed capacities (Setting available beds to 0 will reject hospital from dispatch selection).
        </p>
      </div>

      <div className="card">
        <div className="table-responsive">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Hospital Name</th>
                <th>Address</th>
                <th>Available Beds</th>
                <th>Total Beds</th>
                <th>Specializations</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {hospitals.map((h) => (
                <tr key={h.id}>
                  <td>
                    <strong style={{ color: '#f8fafc' }}>{h.hospital_name}</strong>
                  </td>
                  <td style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{h.address}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <button
                        className="btn"
                        style={{ padding: '0.2rem 0.6rem', background: '#334155' }}
                        onClick={() => handleBedChange(h.id, -1)}
                      >
                        -
                      </button>
                      <span className={`badge ${h.available_beds > 0 ? 'badge-success' : 'badge-danger'}`} style={{ fontSize: '1rem' }}>
                        {h.available_beds}
                      </span>
                      <button
                        className="btn"
                        style={{ padding: '0.2rem 0.6rem', background: '#334155' }}
                        onClick={() => handleBedChange(h.id, 1)}
                      >
                        +
                      </button>
                    </div>
                  </td>
                  <td>{h.total_beds}</td>
                  <td style={{ fontSize: '0.8rem', color: '#38bdf8' }}>{h.specializations}</td>
                  <td>
                    <button
                      className="btn btn-primary"
                      style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
                      onClick={() => handleSaveBeds(h.id, h.available_beds)}
                      disabled={savingId === h.id}
                    >
                      <Save size={14} />
                      {savingId === h.id ? "Saving..." : "Save Beds"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
