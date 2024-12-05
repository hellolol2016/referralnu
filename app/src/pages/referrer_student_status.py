import logging
import streamlit as st
import requests

# Base API URL
BASE_API_URL = "http://localhost:4000/requests/referrer"

# Configure logger
logger = logging.getLogger(__name__)

# Streamlit App Title
st.title("View and Update Student Application Status")

# Function to get application statuses for a referrer
def get_application_status(referrer_id):
    try:
        # Construct the API URL
        url = f"{BASE_API_URL}/{referrer_id}"
        st.write(f"Fetching from URL: {url}")  # Debugging
        response = requests.get(url)

        # Check response status and return JSON data if successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "No application statuses found for the given Referrer ID."}
        else:
            return {"error": f"Failed to retrieve application statuses: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Function to update the application status
def update_application_status(referrer_id, student_id, new_status):
    try:
        # Construct the API URL
        url = f"{BASE_API_URL}/{referrer_id}/students/{student_id}"
        payload = {"applicationStatus": new_status}

        response = requests.put(url, json=payload)

        # Check response status and return a success or error message
        if response.status_code == 200:
            return {"message": "Application status updated successfully."}
        elif response.status_code == 404:
            return {"error": "Student not found. Please check the Referrer ID and Student ID."}
        else:
            return {"error": f"Failed to update application status: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Input fields for Referrer ID and Student ID
referrer_id = st.text_input("Enter Referrer ID")
student_id = st.text_input("Enter Student ID")

# View application status
if st.button("View Application Status"):
    if not referrer_id or not student_id:
        st.warning("Both Referrer ID and Student ID are required.")
    else:
        # Fetch all application statuses for the referrer
        result = get_application_status(referrer_id)

        # Display the result
        if "error" in result:
            st.error(result["error"])
        else:
            # Filter the specific student's status
            student_status = next(
                (status for status in result if str(status.get("studentId")) == student_id),
                None
            )

            if student_status:
                st.subheader("Application Status")
                st.markdown(f"**Referrer ID:** {referrer_id}")
                st.markdown(f"**Student ID:** {student_id}")
                st.markdown(f"**Status:** {student_status.get('applicationStatus', 'N/A')}")

                # Allow user to update the application status
                new_status = st.text_input("Enter New Status for the Application")
                if st.button("Update Application Status"):
                    if not new_status:
                        st.warning("New status is required to update the application.")
                    else:
                        update_result = update_application_status(referrer_id, student_id, new_status)

                        if "error" in update_result:
                            st.error(update_result["error"])
                        else:
                            st.success(update_result["message"])
            else:
                st.error("Application status not found for the given Student ID.")
