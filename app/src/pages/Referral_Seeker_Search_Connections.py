import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Backend API URL
API_URL = "http://web-api:4000/connections"

st.title("Connections Viewer")

# Fetch connections
def fetch_connections():
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch connections: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Main interface
if st.button("Load Connections"):
    connections = fetch_connections()
    if connections:
        st.success("Connections loaded successfully!")
        # Display connections in a table
        st.table(connections)
    else:
        st.warning("No connections found.")
