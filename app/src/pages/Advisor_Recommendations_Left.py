import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Streamlit App Title
st.title("Top Referrers by Remaining Referrals")

# Input for Number of Referrers to Retrieve
num_referrers = st.number_input(
    "Enter the number of top referrers to display:",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

# API Endpoint
api_url = "http://web-api:4000/referrers/left"  # Replace with your actual endpoint

# Fetch Data Button
if st.button("Fetch Top Referrers"):
    # Send GET Request to the Endpoint
    params = {"top_n": num_referrers}  # Pass number of top referrers as query parameter
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        # Convert the API response into a pandas DataFrame for display
        data = response.json()

        # Ensure data is properly formatted before displaying
        if isinstance(data, list) and all(isinstance(row, dict) for row in data):
            df = pd.DataFrame(data)

            if not df.empty:
                # Ensure column order and correct headers
                df = df[["referrerId", "name", "email", "phoneNumber", "numReferrals"]]
                df.columns = ["Referrer ID", "Name", "Email", "Phone Number", "Number of Referrals"]

                # Display the DataFrame in a clean, readable format
                st.subheader(f"Top {num_referrers} Referrers by Remaining Referrals")
                st.table(df)
            else:
                st.warning("No referrer data found.")
        else:
            st.error("Unexpected data format from API.")
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")