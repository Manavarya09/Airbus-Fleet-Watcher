✈️ Airbus Fleet Watcher
A real-time web application to track active Airbus A350 and A380 flights across the globe.

This Streamlit application fetches live flight data from the OpenSky Network, displays the aircraft on an interactive map, and provides a summary dashboard of currently tracked flights.

✨ Features
Live Flight Tracking: Monitors the real-time positions of specified Airbus A350 and A380 aircraft.

Interactive Map: Displays all tracked flights on a Folium map, with custom icons and detailed popups for each aircraft.

Dashboard Metrics: Shows a live count of the total A350s and A380s currently being tracked.

Auto-Refreshing Data: The application automatically fetches fresh data every 60 seconds to stay up-to-date.

Manual Refresh: A "Refresh Data" button allows for immediate data updates.

Detailed Data View: An optional, expandable table to view the raw, processed flight data.

🛠️ Tech Stack
Backend & Web Framework: Streamlit

Data Manipulation: Pandas

API Interaction: Requests

Mapping: Folium & streamlit-folium

Data Source: OpenSky Network API

🚀 Setup and Installation
Follow these steps to get the application running on your local machine.

Prerequisites

Python 3.8 or newer

pip package manager

1. Clone the Repository or Create the Project

First, create a project folder and add all the necessary files (app.py, requirements.txt, etc.).

mkdir airbus_watcher
cd airbus_watcher

2. Create and Activate a Virtual Environment (Recommended)

This step isolates the project's dependencies from your system's Python environment.

# Create the virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

3. Install Dependencies

Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt

4. Run the Application

Launch the Streamlit server.

streamlit run app.py

Your default web browser should open a new tab with the application running at http://localhost:8501.

📂 File Structure
Here is an overview of the project's file structure:

airbus_watcher/
│
├── 📜 requirements.txt        # Lists all Python dependencies for the project.
├── ✈️ aircraft_data.csv       # A sample database of aircraft to track (ICAO24 code and model).
├── ⚙️ config.py               # Stores constants like API URLs, file paths, and model settings.
├── 📦 data_handler.py         # Module for fetching and processing data from the OpenSky Network API.
├── 🗺️ map_generator.py        # Module for creating the interactive Folium map.
├── 🖥️ app.py                  # The main Streamlit application file that ties everything together.
└── 📄 README.md               # This file.

DataSource
This application relies on publicly available data from the OpenSky Network. Please be mindful of their usage policies.

