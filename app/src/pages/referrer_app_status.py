# 4.3

import logging
import streamlit as st
import requests

# Backend API URL for updating status
UPDATE_STATUS_URL = "http://web-api:4000/status"

# Setup logging
logger = logging.getLogger(__name__)

# Page Title
st.title("Change Application Status")

# Function to update request status
def update_request_status(request_id, pending_status):
    try:
        # API call to update the request status
        payload = {"pendingStatus": pending_status}
        url = f"{UPDATE_STATUS_URL}/{request_id}"  # Append requestId to the URL
        response = requests.put(url, json=payload)

        if response.status_code == 200:
            st.success(f"Request ID {request_id} status updated to '{pending_status}' successfully!")
        else:
            st.error(f"Failed to update request status: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Input for Request ID and Pending Status
request_id = st.text_input("Enter Request ID", help="Enter the unique ID of the request")
pending_status = st.selectbox(
    "Select New Status",
    options=["Pending", "Approved", "Rejected"],
    index=0,
    help="Select the new pending status for the request"
)

# Button to update status
if st.button("Update Status"):
    if request_id and pending_status:
        update_request_status(request_id, pending_status.lower())
    else:
        st.warning("Please provide both Request ID and a valid status.")
