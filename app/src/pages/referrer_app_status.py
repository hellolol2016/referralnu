import streamlit as st
import requests

# Base API URL
BASE_API_URL = "http://web-api:4000/requests/student"

# Streamlit App Title
st.title("View Request Details by Student ID")

# Input for Student ID
student_id = st.text_input("Enter Student ID")

# Fetch and display request details
if st.button("Fetch Request Details"):
    if not student_id:
        st.warning("Please enter a Student ID.")
    else:
        try:
            url = f"{BASE_API_URL}/{student_id}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.subheader("Request Details")
                st.write("Debug: API Response")
                st.write(data)  # Debugging step

                if data:
                    for item in data:
                        # Safely retrieve fields with default values if missing
                        pending_status = item.get('pendingStatus', 'Not Available')
                        first_name = item.get('firstName', 'Unknown')
                        last_name = item.get('lastName', 'Unknown')

                        st.markdown(f"**Pending Status:** {pending_status}")
                        st.markdown(f"**Student Name:** {first_name} {last_name}")
                        st.markdown("---")
                else:
                    st.warning("No requests found for the given Student ID.")
            elif response.status_code == 404:
                st.warning("No requests found for the given Student ID.")
            else:
                st.error(f"Failed to fetch request details. HTTP Status: {response.status_code}")
        except Exception as e:
            st.error(f"Error fetching request details: {str(e)}")
