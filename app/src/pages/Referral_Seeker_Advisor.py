import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

API_BASE_URL = "http://web-api:4000/advisors"

# Page title
st.title("Find an Advisor")

# Subtitle and instructions
st.markdown("""
Referral seekers can use this page to find advisors who can guide them. Simply enter the advisor ID to fetch their information.
""")

# Add input field for the advisor ID
advisorID = st.text_input("Enter Advisor ID")

# Create a button to fetch the advisor information
if st.button("Fetch Advisor Info"):
    if advisorID:
        # Make the API request to get advisor info, using `advisorId`
        try:
            response = requests.get(f"{API_BASE_URL}/{advisorID}")  # Send advisor_id as advisorId in the URL
            if response.status_code == 200:
                # Parse the response and display the advisor's information
                data = response.json().get('advisor', [])
                if data:
                    advisor = data[0]  # Assuming the data contains only one result
                    st.subheader(f"Advisor: {advisor['firstName']} {advisor['lastName']}")
                    st.write(f"**Email:** {advisor['email']}")
                    st.write(f"**Phone Number:** {advisor['phoneNumber']}")
                    st.write(f"**College:** {advisor['college']}")
                else:
                    st.warning("No advisor found with this ID.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"API request failed: {e}")
    else:
        st.error("Please enter a valid Advisor ID.")