# config.py

# URL for the OpenSky Network API states endpoint
OPENSKY_URL = "https://opensky-network.org/api/states/all"

# Path to the aircraft database file
AIRCRAFT_DATA_FILE = "aircraft_data.csv"

# Aircraft model information (for map icons)
AIRCRAFT_MODELS = {
    "A350": {
        "color": "blue",
        "icon": "plane"
    },
    "A380": {
        "color": "red",
        "icon": "plane"
    }
}

# Column names from the OpenSky API response (indices)
# See: https://opensky-network.org/apidoc/rest.html#all-state-vectors
STATE_VECTOR_COLUMNS = [
    'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
    'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity',
    'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk',
    'spi', 'position_source'
]
