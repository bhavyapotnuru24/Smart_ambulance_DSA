import React, { useState, useEffect } from 'react';
import { Stethoscope, Check, X } from 'lucide-react';
import { getDoctors, toggleDoctorAvailability } from '../services/api';

export default function ManageDoctors() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDoctors = () => {
    setLoading(true);
    getDoctors()
      .then((res) => setDoctors(res.data))
      .catch((err) => console.error("Failed to load doctors:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDoctors();
  }, []);

  const handleToggle = async (id) => {
    try {
      await toggleDoctorAvailability(id);
      fetchDoctors();
    } catch (err) {
      console.error("Failed to toggle availability:", err);
    }
  };

  if (loading) return <div style={{ padding: '2rem' }}>Loading Doctors Roster...</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#f8fafc' }}>Doctor Roster Management</h2>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Doctor availability feeds into Bipartite Matching for patient emergency assignment.
        </p>
      </div>

      <div className="card">
        <div className="table-responsive">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Doctor Name</th>
                <th>Specialization</th>
                <th>Hospital</th>
                <th>Status</th>
                <th>Toggle Availability</th>
              </tr>
            </thead>
            <tbody>
              {doctors.map((d) => (
                <tr key={d.id}>
                  <td>
                    <strong style={{ color: '#f8fafc' }}>{d.name}</strong>
                  </td>
                  <td style={{ color: '#38bdf8' }}>{d.specialization}</td>
                  <td style={{ fontSize: '0.85rem', color: '#94a3b8' }}>{d.hospital_name || 'N/A'}</td>
                  <td>
                    <span className={`badge ${d.is_available ? 'badge-success' : 'badge-danger'}`}>
                      {d.is_available ? 'Available' : 'On Leave'}
                    </span>
                  </td>
                  <td>
                    <button
                      className={`btn ${d.is_available ? 'btn-danger' : 'btn-success'}`}
                      style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
                      onClick={() => handleToggle(d.id)}
                    >
                      {d.is_available ? <X size={14} /> : <Check size={14} />}
                      {d.is_available ? 'Mark Unavailable' : 'Mark Available'}
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
