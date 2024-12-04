import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
#from streamlit_modal import Modal

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

referrer_endpoint = "http://web-api:4000/referrers"

st.title(f"Get Best Referrers")
st.write('')
st.write('')
st.write('### Which Method Would You Like to Look For Referrers Through')

#modal = Modal(key="top_referrers_modal")

if st.button('Get top referrers', type='primary', use_container_width=True):
    try:
        endpoint = f"{referrer_endpoint}/top"
        logger.debug(endpoint)
        response = requests.get(endpoint)
        data = response.json()
        if data:
            st.success("Results Fetched Successfully!")
            df = pd.DataFrame(data)
            st.subheader("Top Referrers")
            st.table(df)
    except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for top referrers: {e}")
            st.error(f"Failed to fetch student results. Please try again later.")

if st.button('Referrers with the Most Referrals Left to Give', type='primary', use_container_width=True):
     try:
        endpoint = f"{referrer_endpoint}/least"
        logger.debug(endpoint)
        response = requests.get(endpoint)
        data = response.json()
        if data:
            st.success("Results Fetched Successfully!")
            df = pd.DataFrame(data)
            st.subheader("Referrers with the Most Referrals Left to Give")
            st.table(df)
     except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for top referrers: {e}")
            st.error(f"Failed to fetch student results. Please try again later.")
