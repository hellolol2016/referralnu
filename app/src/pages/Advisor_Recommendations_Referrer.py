import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

referrer_endpoint = "http://web-api:4000/referrers"


if st.button('Get top referrers', type='primary', use_container_width=True):
    try:
        endpoint = f"{referrer_endpoint}/top"
        logger.debug(endpoint)
        response = requests.get(endpoint)
        data = response.json()
        if data:
            st.success("Results Fetched Successfully!")
            st.json(data) 
        else:
            st.warning("No data found for the given Student ID.")
    except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for top referrers: {e}")
            st.error(f"Failed to fetch student results. Please try again later.")