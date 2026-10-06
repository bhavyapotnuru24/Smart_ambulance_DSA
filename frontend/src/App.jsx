import React, { useState } from 'react';
import Navbar from './components/Navbar';
import UserHome from './pages/UserHome';
import EmergencyStatus from './pages/EmergencyStatus';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import ManageHospitals from './pages/ManageHospitals';
import ManageDoctors from './pages/ManageDoctors';
import ManageAmbulances from './pages/ManageAmbulances';

export default function App() {
  const [activeTab, setActiveTab] = useState('user-home');
  const [isAdmin, setIsAdmin] = useState(false);
  const [dispatchResult, setDispatchResult] = useState(null);

  return (
    <div className="app-container">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isAdmin={isAdmin}
        setIsAdmin={setIsAdmin}
      />

      <main className="main-content">
        {activeTab === 'user-home' && (
          <UserHome
            setDispatchResult={setDispatchResult}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'emergency-status' && (
          <EmergencyStatus
            dispatchResult={dispatchResult}
            setActiveTab={setActiveTab}
            setDispatchResult={setDispatchResult}
          />
        )}

        {activeTab === 'admin-login' && (
          <AdminLogin
            setIsAdmin={setIsAdmin}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'admin-dashboard' && isAdmin && (
          <AdminDashboard setActiveTab={setActiveTab} />
        )}

        {activeTab === 'manage-hospitals' && isAdmin && (
          <ManageHospitals />
        )}

        {activeTab === 'manage-doctors' && isAdmin && (
          <ManageDoctors />
        )}

        {activeTab === 'manage-ambulances' && isAdmin && (
          <ManageAmbulances />
        )}
      </main>
    </div>
  );
}
