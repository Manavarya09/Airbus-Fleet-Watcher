# data_handler.py

import pandas as pd
import requests
import config

def load_aircraft_database():
    """
    Reads the aircraft data from the CSV file into a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing aircraft 'icao24' and 'model' data.
    """
    try:
        df = pd.read_csv(config.AIRCRAFT_DATA_FILE)
        # Ensure icao24 is lowercase for consistent merging
        df['icao24'] = df['icao24'].str.lower()
        return df
    except FileNotFoundError:
        print(f"Error: The file {config.AIRCRAFT_DATA_FILE} was not found.")
        return pd.DataFrame()

def fetch_and_process_flight_data(aircraft_df):
    """
    Fetches live flight data from OpenSky, filters for tracked aircraft,
    and merges it with the local aircraft database.

    Args:
        aircraft_df (pd.DataFrame): DataFrame of aircraft to track.

    Returns:
        pd.DataFrame: A clean DataFrame of active flights for tracked aircraft.
                      Returns an empty DataFrame if the API call fails or no flights are found.
    """
    # Create a set of ICAO codes for efficient filtering
    tracked_icao_codes = set(aircraft_df['icao24'])

    try:
        # Fetch data from the OpenSky Network API
        response = requests.get(config.OPENSKY_URL)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response
        all_states = response.json().get('states', [])
        if not all_states:
            return pd.DataFrame() # Return empty if no states are received

        # Filter the states in memory before creating a DataFrame for performance
        flight_data = [state for state in all_states if state[0] in tracked_icao_codes]
        
        if not flight_data:
            return pd.DataFrame() # Return empty if none of our aircraft are flying

        # Create a DataFrame from the filtered flight data
        live_df = pd.DataFrame(flight_data, columns=config.STATE_VECTOR_COLUMNS)

        # --- Data Cleaning ---
        # 1. Filter out aircraft that are on the ground
        live_df = live_df[~live_df['on_ground']]
        
        # 2. Merge with our aircraft database to get the model
        merged_df = pd.merge(live_df, aircraft_df, on='icao24', how='inner')
        
        # 3. Clean up callsign strings
        merged_df['callsign'] = merged_df['callsign'].str.strip()

        # 4. Ensure essential numeric columns are of the correct type
        for col in ['longitude', 'latitude', 'baro_altitude', 'velocity', 'true_track']:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
        
        # 5. Drop rows with no location data, as they can't be mapped
        merged_df.dropna(subset=['latitude', 'longitude'], inplace=True)

        return merged_df

    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()
