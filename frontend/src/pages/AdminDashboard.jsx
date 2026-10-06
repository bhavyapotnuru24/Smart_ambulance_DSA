import React, { useState, useEffect } from 'react';
import { Hospital, Truck, Stethoscope, ShieldAlert, CheckCircle, AlertTriangle, Activity } from 'lucide-react';
import { getDashboardStats } from '../services/api';

export default function AdminDashboard({ setActiveTab }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardStats()
      .then((res) => setStats(res.data))
      .catch((err) => console.error("Failed to load dashboard stats:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '3rem' }}>Loading Admin Dashboard Metrics...</div>;
  }

  if (!stats) return <div>Failed to load dashboard metrics.</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#f8fafc' }}>Admin Overview Dashboard</h2>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Real-time resource capacity & dispatch system metrics</p>
        </div>
      </div>

      {/* Grid of 4 Key Stats */}
      <div className="grid-4">
        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'rgba(2, 132, 199, 0.15)', color: '#38bdf8' }}>
            <Hospital />
          </div>
          <div>
            <div className="metric-value">{stats.total_hospitals}</div>
            <div className="metric-label">Total Hospitals</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' }}>
            <CheckCircle />
          </div>
          <div>
            <div className="metric-value">{stats.hospitals_with_available_beds}</div>
            <div className="metric-label">Hospitals w/ Beds</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#fca5a5' }}>
            <AlertTriangle />
          </div>
          <div>
            <div className="metric-value">{stats.hospitals_zero_beds}</div>
            <div className="metric-label">Zero-Bed Hospitals</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#fcd34d' }}>
            <Activity />
          </div>
          <div>
            <div className="metric-value">{stats.active_emergencies}</div>
            <div className="metric-label">Active Emergencies</div>
          </div>
        </div>
      </div>

      {/* Ambulance & Doctor Cards */}
      <div className="grid-2">
        {/* Ambulance System Breakdown (6 Predefined Units) */}
        <div className="card">
          <div className="card-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Truck size={22} color="#38bdf8" />
              <span>Ambulance Status (6 Predefined Units)</span>
            </div>
            <button className="btn btn-primary" onClick={() => setActiveTab('manage-ambulances')} style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem' }}>
              Manage
            </button>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: '#0f172a', borderRadius: '8px' }}>
              <span>Available Ambulances</span>
              <span className="badge badge-success" style={{ fontSize: '1rem' }}>{stats.available_ambulances} / 6</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: '#0f172a', borderRadius: '8px' }}>
              <span>Busy Ambulances</span>
              <span className="badge badge-danger" style={{ fontSize: '1rem' }}>{stats.busy_ambulances} / 6</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: '#0f172a', borderRadius: '8px' }}>
              <span>Currently Dispatched</span>
              <span className="badge badge-info" style={{ fontSize: '1rem' }}>{stats.dispatched_ambulances}</span>
            </div>
          </div>
        </div>

        {/* Doctor Roster Summary */}
        <div className="card">
          <div className="card-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Stethoscope size={22} color="#10b981" />
              <span>Medical Roster & Doctors</span>
            </div>
            <button className="btn btn-primary" onClick={() => setActiveTab('manage-doctors')} style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem' }}>
              Manage
            </button>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: '#0f172a', borderRadius: '8px' }}>
              <span>Total Doctors</span>
              <span style={{ fontWeight: '700', color: '#f8fafc', fontSize: '1.1rem' }}>{stats.total_doctors}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: '#0f172a', borderRadius: '8px' }}>
              <span>Available Duty Doctors</span>
              <span className="badge badge-success" style={{ fontSize: '1rem' }}>{stats.available_doctors} Available</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
