"""
Google Maps Service
Days 22-24: Commute Calculator - Maps Integration

Handles all Google Maps API interactions:
- Distance Matrix API for commute calculations
- Geocoding (future)
- Places API (future)
"""

import googlemaps
from typing import Optional, Dict, Any
import os
from datetime import datetime

class MapsService:
    """
    Google Maps API integration service

    For Phase 2 MVP, we'll use a mock implementation to avoid API costs during development.
    Switch to real API key in production.
    """

    def __init__(self, api_key: Optional[str] = None, use_mock: bool = True):
        """
        Initialize Maps Service

        Args:
            api_key: Google Maps API key (optional if using mock)
            use_mock: If True, returns mock data instead of calling real API
        """
        self.use_mock = use_mock

        if not use_mock:
            if not api_key:
                api_key = os.getenv("GOOGLE_MAPS_API_KEY")

            if not api_key:
                raise ValueError("Google Maps API key required when not using mock mode")

            self.client = googlemaps.Client(key=api_key)
        else:
            self.client = None

    def calculate_commute(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        mode: str = "driving",
        departure_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculate commute time between two points

        Args:
            origin_lat: Origin latitude (work location)
            origin_lng: Origin longitude
            dest_lat: Destination latitude (property)
            dest_lng: Destination longitude
            mode: Travel mode (driving, transit, walking, bicycling)
            departure_time: When to depart (for traffic estimates)

        Returns:
            Dict containing distance and duration information
        """

        if self.use_mock:
            return self._mock_commute_calculation(
                origin_lat, origin_lng,
                dest_lat, dest_lng,
                mode
            )

        # Real Google Maps API call
        origin = f"{origin_lat},{origin_lng}"
        destination = f"{dest_lat},{dest_lng}"

        # Use current time if not specified
        if not departure_time:
            departure_time = datetime.now()

        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode=mode,
                departure_time=departure_time,
                traffic_model="best_guess"
            )

            # Extract data from response
            if result['status'] == 'OK':
                element = result['rows'][0]['elements'][0]

                if element['status'] == 'OK':
                    return {
                        'distance_meters': element['distance']['value'],
                        'distance_text': element['distance']['text'],
                        'duration_seconds': element['duration']['value'],
                        'duration_text': element['duration']['text'],
                        'duration_in_traffic_seconds': element.get('duration_in_traffic', {}).get('value'),
                        'duration_in_traffic_text': element.get('duration_in_traffic', {}).get('text'),
                    }
                else:
                    raise Exception(f"Route not found: {element['status']}")
            else:
                raise Exception(f"Distance Matrix API error: {result['status']}")

        except Exception as e:
            raise Exception(f"Failed to calculate commute: {str(e)}")

    def _mock_commute_calculation(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        mode: str
    ) -> Dict[str, Any]:
        """
        Mock commute calculation for development

        Calculates approximate time based on straight-line distance
        """
        # Calculate approximate distance using Haversine formula
        from math import radians, cos, sin, asin, sqrt

        # Convert to radians
        lon1, lat1, lon2, lat2 = map(radians, [origin_lng, origin_lat, dest_lng, dest_lat])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers
        r = 6371
        distance_km = c * r
        distance_meters = int(distance_km * 1000)

        # Estimate time based on mode
        speed_kmh = {
            'driving': 40,      # Average city driving speed
            'transit': 25,      # Public transit
            'walking': 5,       # Walking speed
            'bicycling': 15,    # Cycling speed
        }

        avg_speed = speed_kmh.get(mode, 40)
        duration_hours = distance_km / avg_speed
        duration_seconds = int(duration_hours * 3600)

        # Add traffic for driving (20% increase)
        duration_in_traffic_seconds = None
        duration_in_traffic_text = None

        if mode == 'driving':
            duration_in_traffic_seconds = int(duration_seconds * 1.2)
            duration_in_traffic_text = self._format_duration(duration_in_traffic_seconds)

        return {
            'distance_meters': distance_meters,
            'distance_text': f"{distance_km:.1f} km",
            'duration_seconds': duration_seconds,
            'duration_text': self._format_duration(duration_seconds),
            'duration_in_traffic_seconds': duration_in_traffic_seconds,
            'duration_in_traffic_text': duration_in_traffic_text,
        }

    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to human-readable text"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {minutes} min{'s' if minutes != 1 else ''}"
        else:
            return f"{minutes} min{'s' if minutes != 1 else ''}"


# Singleton instance
_maps_service = None

def get_maps_service(use_mock: bool = True) -> MapsService:
    """Get or create the MapsService singleton"""
    global _maps_service
    if _maps_service is None:
        _maps_service = MapsService(use_mock=use_mock)
    return _maps_service
