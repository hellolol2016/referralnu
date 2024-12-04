import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

# Base URL for the API
API_BASE_URL = "http://web-api:4000/requests"

# Title and introduction
st.title("Referral Request Management")
st.markdown("""
Welcome to the Referral Request portal. Here you can view, create, and update referral requests.
Choose a functionality from the sidebar to get started.
""")

# Sidebar Navigation
menu = st.sidebar.selectbox("Choose a functionality", ["View Requests", "Create Request", "Update Request Status"])

# Handling "View Requests" functionality
if menu == "View Requests":
    st.header("View Requests by Status")

    # Input for request status
    status = st.text_input("Enter Request Status", "Pending", placeholder="e.g., 'Pending', 'Accepted', 'Rejected'")

    if st.button("Fetch Requests"):
        if status:
            try:
                response = requests.get(f"{API_BASE_URL}/{status}")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        st.write(f"**Found {len(data)} requests with status '{status}':**")

                        df = pd.DataFrame(data)

                        # Clean up column names (if needed)
                        df.columns = [col.replace('_', ' ').title() for col in df.columns]

                        # Display the data in a table format
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning(f"No requests found with status '{status}'.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"API request failed: {e}")
        else:
            st.error("Please enter a valid status.")

# Handling "Create Request" functionality
elif menu == "Create Request":
    st.header("Create a New Referral Request")

    # Input fields for creating a new request
    student_id = st.text_input("Student ID", placeholder="Enter your student ID")
    company_id = st.text_input("Company ID", placeholder="Enter the company's ID")
    pending_status = st.text_input("Request Status", "Pending", placeholder="Optional, default: 'Pending'")

    # Submit button to create a request
    if st.button("Submit Request"):
        if student_id and company_id:
            try:
                payload = {
                    "studentId": student_id,
                    "companyId": company_id,
                    "pendingStatus": pending_status
                }
                response = requests.post(f"{API_BASE_URL}/info", json=payload)
                if response.status_code == 201:
                    st.success("Request created successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"API request failed: {e}")
        else:
            st.error("Please fill in all required fields: Student ID and Company ID.")

# Handling "Update Request Status" functionality
elif menu == "Update Request Status":
    st.header("Update Request Status")

    # Input fields
    request_id = st.text_input("Request ID", placeholder="Enter the request ID")
    new_status = st.text_input("New Status", "Pending", placeholder="e.g., 'Pending', 'Accepted', 'Rejected'")

    # Update status button
    if st.button("Update Status"):
        if request_id and new_status:
            try:
                response = requests.put(f"{API_BASE_URL}/status/{request_id}", json={"status": new_status})
                if response.status_code == 200:
                    st.success("Request status updated successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"API request failed: {e}")
        else:
            st.error("Please provide both Request ID and New Status.")
