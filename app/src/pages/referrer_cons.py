# 4.4

import logging
import streamlit as st
import requests

# Backend API URL for creating connections
BASE_API_URL = "http://web-api:4000"
CREATE_CONNECTION_URL = "http://web-api:4000/connections"

# Setup logging
logger = logging.getLogger(__name__)

# Page Title
st.title("Communicate Requirements")

# Function to create a new connection
def create_connection(request_id, student_id, referrer_id):
    try:
        # API call to create the connection
        payload = {
            "studentId": student_id,
            "referrerId": referrer_id
        }
        endpoint = f"{CREATE_CONNECTION_URL}/{request_id}"
        response = requests.post(endpoint, json=payload)

        if response.status_code == 201:
            st.success("Connection created successfully!")
        else:
            st.error(f"Failed to create connection: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Input fields for connection data
request_id = st.text_input("Enter Request ID", help="Enter the unique ID of the request")
student_id = st.text_input("Enter Student ID", help="Enter the unique ID of the student")
referrer_id = st.text_input("Enter Referrer ID", help="Enter the unique ID of the referrer")

# Button to create a connection
if st.button("Create Connection"):
    if request_id and student_id and referrer_id:
        try:
            # Ensure all IDs are valid integers
            request_id = int(request_id)
            student_id = int(student_id)
            referrer_id = int(referrer_id)
            create_connection(request_id, student_id, referrer_id)
        except ValueError:
            st.error("All IDs must be valid numbers.")
    else:
        st.warning("Please provide all required fields: Request ID, Student ID, and Referrer ID.")
