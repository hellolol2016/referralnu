import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

referrer_endpoint = "http://web-api:4000/referrers"

st.title("Get Best Referrers")
st.write("### Which Method Would You Like to Look For Referrers Through")

# Encapsulate the first action in a collapsible container
with st.expander("Get top referrers"):
    top_n = st.slider("Select number of referrers", min_value=1, max_value=10, value=5, key="top_referrers_slider")
    if st.button("Fetch Top Referrers", type="primary", use_container_width=True, key="top_referrers_button"):
        # Send a GET request to the /best endpoint
        try:
            response = requests.get(f"{referrer_endpoint}/best", params={"top_n": top_n})
            if response.status_code == 200:
                data = response.json()  # Parse the JSON data
                if data:
                    # Convert the JSON response into a pandas DataFrame for easier handling
                    df = pd.DataFrame(data)
                    # Display the dataframe in Streamlit
                    st.write(f"Referrer Information for Top {top_n} Companies")
                    st.dataframe(df)
                else:
                    st.write("No referrer data found for the top companies.")
            else:
                st.error(f"Failed to fetch data. Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {str(e)}")

# Encapsulate the second action in another collapsible container
with st.expander("Referrers with the Most Referrals Left to Give"):
    num_referrers = st.slider("Select number of top companies", min_value=1, max_value=10, value=5, key="most_referrals_slider")
    if st.button("Fetch Referrers by Referrals Left", type="primary", use_container_width=True, key="most_referrals_button"):
        # Send GET Request to the Endpoint
        params = {"top_n": num_referrers}  # Pass number of top referrers as query parameter
        try:
            response = requests.get(f"{referrer_endpoint}/left", params=params)
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
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {str(e)}")

