import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()




# API Endpoint
api_url = "http://web-api:4000/referrers/best"  # Replace with your actual endpoint

st.title("Referrer Information for Top N Companies")

# Add a slider to select the number of top companies to display
top_n = st.slider("Select number of top companies", min_value=1, max_value=10, value=5)

# Send a GET request to the /best endpoint
try:
    response = requests.get(api_url, params={"top_n": top_n})

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
