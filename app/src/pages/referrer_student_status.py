# 4.5

import logging
import streamlit as st
import requests

# Base API URL
BASE_API_URL = "http://web-api:4000/referrer"

# Configure logger
logger = logging.getLogger(__name__)

# Streamlit App Title
st.title("Manage Referrer-Student Status")

# Function to get student status for a referrer
def get_student_status(referrer_id, student_id):
    try:
        response = requests.get(f"{BASE_API_URL}/{referrer_id}/students/{student_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to retrieve student status: {response.status_code}")
            st.write(response.text)
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Function to update student status for a referrer
def update_student_status(referrer_id, student_id, status):
    payload = {"status": status}
    try:
        response = requests.put(f"{BASE_API_URL}/{referrer_id}/students/{student_id}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to update student status: {response.status_code}")
            st.write(response.text)
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Input fields
referrer_id = st.text_input("Enter Referrer ID")
student_id = st.text_input("Enter Student ID")

# View student status
if st.button("View Student Status"):
    if not referrer_id or not student_id:
        st.warning("Referrer ID and Student ID are required.")
    else:
        result = get_student_status(referrer_id, student_id)
        if result:
            st.success("Student status retrieved successfully!")
            st.json(result)

# Update student status
new_status = st.text_input("Enter New Status for Student (optional)")
if st.button("Update Student Status"):
    if not referrer_id or not student_id or not new_status:
        st.warning("Referrer ID, Student ID, and New Status are required to update the status.")
    else:
        result = update_student_status(referrer_id, student_id, new_status)
        if result:
            st.success("Student status updated successfully!")
            st.json(result)
