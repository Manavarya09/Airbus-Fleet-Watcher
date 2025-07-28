# app.py

import streamlit as st
from streamlit_folium import st_folium
import data_handler
import map_generator
import time
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Airbus Fleet Watcher",
    page_icon="✈️",
    layout="wide"
)

# --- Caching Data Fetching ---
@st.cache_data(ttl=60)
def get_flight_data():
    """
    Cached function to fetch and process flight data.
    Cache expires every 60 seconds.
    """
    print("Fetching new data...")
    aircraft_db = data_handler.load_aircraft_database()
    if aircraft_db.empty:
        st.error("Could not load aircraft database. Please check `aircraft_data.csv`.")
        return None
    
    flight_df = data_handler.fetch_and_process_flight_data(aircraft_db)
    return flight_df

# --- Main Application ---
st.title("✈️ Airbus A350 & A380 Fleet Watcher")
st.markdown(f"**User Location:** Dubai, UAE | **Date:** {datetime.now().strftime('%A, %B %d, %Y')}")

# --- Controls: Refresh Button and Last Updated Timestamp ---
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

with col2:
    last_updated_time = time.time()
    st.info(f"Data automatically refreshes every 60 seconds. Last update: {datetime.fromtimestamp(last_updated_time).strftime('%H:%M:%S')}")

# Fetch data using the cached function
flight_data = get_flight_data()

if flight_data is None or flight_data.empty:
    st.warning("No tracked aircraft are currently airborne or data could not be retrieved from the API.")
else:
    # --- Key Metrics Dashboard ---
    st.markdown("### 📊 Live Flight Summary")
    
    a350_count = flight_data[flight_data['model'] == 'A350'].shape[0]
    a380_count = flight_data[flight_data['model'] == 'A380'].shape[0]

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric(label="Airbus A350s Tracked", value=a350_count)
    metric_col2.metric(label="Airbus A380s Tracked", value=a380_count)

    # --- Interactive Map ---
    st.markdown("### 🗺️ Real-Time Flight Map")
    flight_map = map_generator.create_flight_map(flight_data)
    # The `returned_objects` argument is suppressed as we don't need map interactions back in Streamlit
    st_folium(flight_map, width='100%', height=500, returned_objects=[])

    # --- Raw Data Table ---
    if st.checkbox("Show Detailed Flight Data"):
        st.markdown("### 🗂️ Flight Data Details")
        # Display a filtered and reordered view of the dataframe
        display_columns = [
            'callsign', 'model', 'origin_country', 'latitude', 'longitude', 
            'baro_altitude', 'velocity', 'true_track', 'icao24'
        ]
        st.dataframe(flight_data[display_columns])
