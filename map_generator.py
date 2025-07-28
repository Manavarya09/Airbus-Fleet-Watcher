# map_generator.py

import folium
import config

def create_flight_map(flight_df):
    """
    Generates an interactive Folium map displaying the location of each flight.

    Args:
        flight_df (pd.DataFrame): The DataFrame containing processed flight data.

    Returns:
        folium.Map: The generated Folium map object.
    """
    # Initialize map centered on Dubai, UAE
    map_center = [25.276987, 55.296249]
    flight_map = folium.Map(location=map_center, zoom_start=4)

    # Add markers for each aircraft
    for _, flight in flight_df.iterrows():
        model = flight['model']
        model_info = config.AIRCRAFT_MODELS.get(model, {"color": "gray", "icon": "plane"})

        # Create a clean HTML popup
        popup_html = f"""
        <b>Flight:</b> {flight.get('callsign', 'N/A')}<br>
        <b>Aircraft:</b> {model}<br>
        <b>Operator Origin:</b> {flight.get('origin_country', 'N/A')}<br>
        <b>Altitude:</b> {flight.get('baro_altitude', 'N/A')} meters<br>
        <b>Speed:</b> {flight.get('velocity', 'N/A')} m/s<br>
        <b>Lat/Lon:</b> {flight.get('latitude'):.4f}, {flight.get('longitude'):.4f}
        """
        popup = folium.Popup(popup_html, max_width=300)

        # Create and add marker to the map
        folium.Marker(
            location=[flight['latitude'], flight['longitude']],
            popup=popup,
            icon=folium.Icon(color=model_info['color'], icon=model_info['icon'], prefix='fa'),
            tooltip=f"{flight.get('callsign', 'N/A')} ({model})"
        ).add_to(flight_map)

    return flight_map
