// Hyderabad city center fallback coordinates (Jubilee Hills / Banjara Hills)
export const DEFAULT_HYDERABAD_LOCATION = {
  latitude: 17.4320,
  longitude: 78.4050,
  address: "Jubilee Hills Checkpost, Hyderabad (Default Fallback)",
  isFallback: true
};

export const getCurrentLocation = () => {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      console.warn("Geolocation API not supported by browser. Using Hyderabad default.");
      resolve({
        ...DEFAULT_HYDERABAD_LOCATION,
        error: "Geolocation is not supported by your browser."
      });
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          address: `Lat: ${position.coords.latitude.toFixed(4)}, Lng: ${position.coords.longitude.toFixed(4)} (Current Location)`,
          isFallback: false
        });
      },
      (error) => {
        console.warn("Geolocation error or permission denied:", error.message);
        let errorMsg = "Unable to retrieve your location.";
        if (error.code === error.PERMISSION_DENIED) {
          errorMsg = "Location permission denied by user. Using Hyderabad default.";
        }
        resolve({
          ...DEFAULT_HYDERABAD_LOCATION,
          error: errorMsg
        });
      },
      {
        enableHighAccuracy: true,
        timeout: 8000,
        maximumAge: 0
      }
    );
  });
};
