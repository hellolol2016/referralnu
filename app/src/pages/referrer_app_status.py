import streamlit as st
import requests

# Base URLs for API
BASE_API_URL = "http://web-api:4000/requests"
UPDATE_STATUS_URL = "http://web-api:4000/status"

# Sidebar Navigation
tab = st.sidebar.radio("Choose a functionality", ["View Requests", "Update Requests"])

# **View Requests** tab
if tab == "View Requests":
    st.title("View Request Details by Student ID")

    student_id = st.text_input("Enter Student ID", key="view_student_id")

    if st.button("Fetch Request Details", key="fetch_requests_button"):
        if not student_id:
            st.warning("Please enter a Student ID.")
        else:
            try:
                # Fetch all requests from the backend
                response = requests.get(BASE_API_URL)

                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Request Details")

                    # Filter requests based on the provided student ID
                    filtered_data = [item for item in data if str(item.get("studentId")) == student_id]

                    if filtered_data:
                        for item in filtered_data:
                            request_id = item.get("requestId", "N/A")
                            pending_status = item.get("pendingStatus", "Not Available")
                            company_id = item.get("companyId", "Not Available")
                            created_at = item.get("createdAt", "Not Available")

                            st.markdown(f"**Request ID:** {request_id}")
                            st.markdown(f"**Pending Status:** {pending_status}")
                            st.markdown(f"**Company ID:** {company_id}")
                            st.markdown(f"**Created At:** {created_at}")
                            st.markdown("---")
                    else:
                        st.warning("No requests found for the given Student ID.")
                else:
                    st.error(f"Failed to fetch request details. HTTP Status: {response.status_code}")
            except Exception as e:
                st.error(f"Error fetching request details: {str(e)}")

# **Update Requests** tab
elif tab == "Update Requests":
    st.header("Update Request Status")

    # Input fields
    request_id = st.text_input("Request ID", placeholder="Enter the request ID")
    new_status = st.text_input("New Status", placeholder="e.g., 'Pending', 'Accepted', 'Rejected'")

    # Update status button
    if st.button("Update Status"):
        if request_id and new_status:
            try:
                # API call to update request status
                response = requests.put(f"{BASE_API_URL}/status/{request_id}", json={"pendingStatus": new_status})

                # Handle response
                if response.status_code == 200:
                    st.success("Request status updated successfully!")
                    st.json(response.json())  # Display the response JSON for confirmation
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"API request failed: {e}")
        else:
            st.error("Please provide both Request ID and New Status.")
