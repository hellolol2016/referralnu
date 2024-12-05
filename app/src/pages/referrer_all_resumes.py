# 4.1

import logging
import streamlit as st
import requests

# Back button
if st.button("← Back to Referrer Home"):
    st.switch_page("pages/Referrer_Home.py")

BASE_API_URL = "http://web-api:4000/referrer"
GET_STUDENT_REQUESTS_URL = "http://web-api:4000/students"

logger = logging.getLogger(__name__)

st.title("View all Info")

# Function to fetch student information
def fetch_student_requests(student_id):
    try:
        response = requests.get(f"{GET_STUDENT_REQUESTS_URL}/{student_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch student data: {response.status_code}")
            st.write(response.text)
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Input for Student ID
student_id = st.text_input("Enter Student ID")

# Fetch and display the data
if student_id:
    if st.button("Fetch Student Information"):
        # Fetch data from the backend API
        student_requests = fetch_student_requests(student_id)

        if student_requests:
            st.success("Information loaded successfully!")

            # Format and display the data
            st.subheader("Student Information")
            for student in student_requests:
                st.markdown(f"**Student ID:** {student['studentId']}")
                st.markdown(f"**First Name:** {student['firstName']}")
                st.markdown(f"**Last Name:** {student['lastName']}")
                st.markdown("---")
        else:
            st.warning("No information found for the given Student ID.")
else:
    st.warning("Please enter a Student ID.")
