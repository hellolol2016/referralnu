import logging
import streamlit as st
import requests

# Backend API URL
API_URL = "http://web-api:4000/connections"

# Setup logging
logger = logging.getLogger(__name__)

st.title("Connections Viewer")

# Function to fetch connections by studentId
def fetch_connections(student_id):
    try:
        response = requests.get(f"{API_URL}/{student_id}")  # Modify the URL to include studentId
        if response.status_code == 200:
            return response.json()  # Return the connections in JSON format
        else:
            st.error(f"Failed to fetch connections: {response.status_code}")
            st.write(response.text)
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Main interface
student_id = st.text_input("Enter Student ID")

if student_id:
    if st.button("Load Connections"):
        connections = fetch_connections(student_id)
        if connections:
            st.success("Connections loaded successfully!")
            # Display connections in a table
            st.table(connections)
        else:
            st.warning("No connections found.")
else:
    st.warning("Please enter a Student ID.")
