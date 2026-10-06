import React from 'react';
import { Activity, ShieldAlert, LayoutDashboard, Hospital, Stethoscope, Truck } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, isAdmin, setIsAdmin }) {
  return (
    <nav className="navbar">
      <div className="nav-brand" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('user-home')}>
        <Activity size={28} color="#38bdf8" />
        <span>SMART AMBULANCE DISPATCH</span>
      </div>

      <div className="nav-links">
        <button
          className={`nav-btn emergency ${activeTab === 'user-home' ? 'active' : ''}`}
          onClick={() => setActiveTab('user-home')}
        >
          <ShieldAlert size={18} />
          Report Emergency
        </button>

        {activeTab === 'emergency-status' && (
          <button
            className="nav-btn active"
            onClick={() => setActiveTab('emergency-status')}
          >
            <Activity size={18} />
            Live Status
          </button>
        )}

        {!isAdmin ? (
          <button
            className={`nav-btn ${activeTab === 'admin-login' ? 'active' : ''}`}
            onClick={() => setActiveTab('admin-login')}
          >
            <LayoutDashboard size={18} />
            Admin Login
          </button>
        ) : (
          <>
            <button
              className={`nav-btn ${activeTab === 'admin-dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('admin-dashboard')}
            >
              <LayoutDashboard size={18} />
              Dashboard
            </button>
            <button
              className={`nav-btn ${activeTab === 'manage-hospitals' ? 'active' : ''}`}
              onClick={() => setActiveTab('manage-hospitals')}
            >
              <Hospital size={18} />
              Hospitals
            </button>
            <button
              className={`nav-btn ${activeTab === 'manage-doctors' ? 'active' : ''}`}
              onClick={() => setActiveTab('manage-doctors')}
            >
              <Stethoscope size={18} />
              Doctors
            </button>
            <button
              className={`nav-btn ${activeTab === 'manage-ambulances' ? 'active' : ''}`}
              onClick={() => setActiveTab('manage-ambulances')}
            >
              <Truck size={18} />
              Ambulances
            </button>
            <button
              className="nav-btn"
              onClick={() => {
                setIsAdmin(false);
                setActiveTab('user-home');
              }}
              style={{ color: '#ef4444' }}
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
