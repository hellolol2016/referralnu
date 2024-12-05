# 4.6

import logging
import streamlit as st
import requests

# Base API URL
BASE_API_URL = "http://web-api:4000/referrer"

# Configure logger
logger = logging.getLogger(__name__)

# App Title
st.title("Update Referrer Information")

# Function to update referrer information
def update_referrer_info(referrer_id, name, email, phone_number):
    payload = {
        "name": name,
        "email": email,
        "phoneNumber": phone_number
    }
    try:
        response = requests.put(f"{BASE_API_URL}/{referrer_id}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

# Input fields for updating referrer information
referrer_id = st.text_input("Enter Referrer ID")
name = st.text_input("Enter Name")
email = st.text_input("Enter Email")
phone_number = st.text_input("Enter Phone Number")

# Update button
if st.button("Update Referrer Information"):
    # Validate inputs
    if not referrer_id or not name or not email or not phone_number:
        st.warning("All fields are required to update referrer information.")
    else:
        # Call the update function
        result = update_referrer_info(referrer_id, name, email, phone_number)

        # Always display the new information entered
        st.subheader("New Information")
        st.markdown(f"**Referrer ID:** {referrer_id}")
        st.markdown(f"**Name:** {name}")
        st.markdown(f"**Email:** {email}")
        st.markdown(f"**Phone Number:** {phone_number}")


        # Display the status of the update operation
        # if result:
            # st.success("Referrer information updated successfully!")
        # else:
            # st.error("Referrer information failed to update.")
