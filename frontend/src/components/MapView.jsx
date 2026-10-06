import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';

// Create custom colored markers using SVG icons
const createCustomIcon = (color, label) => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32">
      <path fill="${color}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
      <circle cx="12" cy="9" r="3" fill="#ffffff"/>
      <text x="12" y="9.8" font-size="3" font-weight="bold" fill="${color}" text-anchor="middle">${label}</text>
    </svg>
  `;
  return L.divIcon({
    html: svg,
    className: 'custom-leaflet-marker',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  });
};

const userIcon = createCustomIcon('#38bdf8', 'U');
const availableAmbIcon = createCustomIcon('#10b981', 'A');
const busyAmbIcon = createCustomIcon('#ef4444', 'B');
const dispatchedAmbIcon = createCustomIcon('#3b82f6', 'D');
const hospitalIcon = createCustomIcon('#dc2626', 'H');

export default function MapView({ userLocation, hospitals = [], ambulances = [], selectedRoute, alternativeRoutes = [] }) {
  // Center of Hyderabad
  const center = userLocation 
    ? [userLocation.latitude, userLocation.longitude] 
    : [17.4320, 78.4050];

  return (
    <div className="map-container">
      <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* User Location Marker */}
        {userLocation && (
          <Marker position={[userLocation.latitude, userLocation.longitude]} icon={userIcon}>
            <Popup>
              <strong>User Emergency Location</strong><br />
              {userLocation.address || `Lat: ${userLocation.latitude.toFixed(4)}, Lng: ${userLocation.longitude.toFixed(4)}`}
            </Popup>
          </Marker>
        )}

        {/* Hospital Markers */}
        {hospitals.map((h) => (
          <Marker key={`hosp-${h.id}`} position={[h.latitude, h.longitude]} icon={hospitalIcon}>
            <Popup>
              <strong>{h.hospital_name}</strong><br />
              {h.address}<br />
              <strong>Available Beds: {h.available_beds}</strong> / {h.total_beds}<br />
              <small>Specializations: {h.specializations}</small>
            </Popup>
          </Marker>
        ))}

        {/* Ambulance Markers */}
        {ambulances.map((a) => {
          let icon = availableAmbIcon;
          if (a.status === 'Busy') icon = busyAmbIcon;
          if (a.status === 'Dispatched') icon = dispatchedAmbIcon;

          return (
            <Marker key={`amb-${a.id}`} position={[a.latitude, a.longitude]} icon={icon}>
              <Popup>
                <strong>Ambulance Unit {a.ambulance_code}</strong><br />
                Status: <strong>{a.status}</strong><br />
                Driver: {a.driver_name || 'N/A'}<br />
                Phone: {a.driver_phone || 'N/A'}
              </Popup>
            </Marker>
          );
        })}

        {/* Alternative Routes Polylines */}
        {alternativeRoutes.map((r, idx) => {
          if (r.is_recommended) return null;
          return (
            <Polyline
              key={`alt-route-${idx}`}
              positions={r.path}
              color="#94a3b8"
              dashArray="6, 6"
              weight={4}
              opacity={0.6}
            />
          );
        })}

        {/* Selected Optimal Route Polyline */}
        {selectedRoute && selectedRoute.path && (
          <Polyline
            positions={selectedRoute.path}
            color="#0284c7"
            weight={6}
            opacity={0.9}
          />
        )}
      </MapContainer>
    </div>
  );
}
