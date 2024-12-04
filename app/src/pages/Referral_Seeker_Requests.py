import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

import streamlit as st
import requests

# Base URL for the API
API_BASE_URL = "http://web-api:4000/requests"

st.title("Your Referral Requests")

# Sidebar Navigation
menu = st.sidebar.selectbox("Choose a functionality", ["View Requests", "Create Request", "Update Request Status"])

if menu == "View Requests":
    st.header("View Requests by Status")

    # Input for request status
    status = st.text_input("Enter Request Status (e.g., 'Pending', 'Accepted', 'Rejected')")

    if st.button("Fetch Requests"):
        try:
            # Call the API endpoint
            response = requests.get(f"{API_BASE_URL}/requests/{status}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"API request failed: {e}")

elif menu == "Create Request":
    st.header("Create a New Request")

    # Input fields
    request_name = st.text_input("Request Name")
    request_details = st.text_area("Request Details")

    if st.button("Submit Request"):
        try:
            # Call the API endpoint
            response = requests.post(f"{API_BASE_URL}/requests", json={"name": request_name, "details": request_details})
            if response.status_code == 201:
                st.success("Request created successfully!")
                st.json(response.json())
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"API request failed: {e}")

elif menu == "Update Request Status":
    st.header("Update Request Status")

    # Input fields
    request_id = st.text_input("Request ID")
    new_status = st.text_input("New Status (e.g., 'Pending', 'Completed')")

    if st.button("Update Status"):
        try:
            # Call the API endpoint
            response = requests.put(f"{API_BASE_URL}/requests/{request_id}", json={"status": new_status})
            if response.status_code == 200:
                st.success("Request status updated successfully!")
                st.json(response.json())
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"API request failed: {e}")
