import React, { useState } from 'react';
import { MapPin, Navigation, AlertCircle, CheckCircle2 } from 'lucide-react';
import { getCurrentLocation } from '../services/location';

export default function LocationPicker({ location, setLocation }) {
  const [loading, setLoading] = useState(false);

  const handleFetchLocation = async () => {
    setLoading(true);
    const loc = await getCurrentLocation();
    setLocation(loc);
    setLoading(false);
  };

  return (
    <div className="card" style={{ background: '#0f172a', borderColor: '#334155' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: '600', color: '#f1f5f9' }}>
            <MapPin size={20} color="#38bdf8" />
            <span>Emergency Location (Auto Detected)</span>
          </div>
          <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.2rem' }}>
            {location ? location.address : "Location not captured yet"}
          </div>
        </div>

        <button
          type="button"
          className="btn btn-primary"
          onClick={handleFetchLocation}
          disabled={loading}
          style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}
        >
          <Navigation size={16} className={loading ? "spin" : ""} />
          {loading ? "Locating..." : location ? "Re-detect Location" : "Detect Location"}
        </button>
      </div>

      {location && (
        <div style={{ marginTop: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem' }}>
          {location.isFallback ? (
            <span className="badge badge-warning">
              <AlertCircle size={14} />
              {location.error || "Using Default Hyderabad Location (GPS Permission Denied / Standalone)"}
            </span>
          ) : (
            <span className="badge badge-success">
              <CheckCircle2 size={14} />
              Live Browser GPS Position Captured ({location.latitude.toFixed(4)}, {location.longitude.toFixed(4)})
            </span>
          )}
        </div>
      )}
    </div>
  );
}
