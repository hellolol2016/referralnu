import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

student_endpoint = "http://web-api:4000/students"

st.title(f"Track Advisor Results")
st.write('')
st.write('')
st.write('### Which Advisor are you')

advisor_id = st.text_input("Enter Advisor ID to fetch results:")

if st.button('Get Advisor Results', type='primary', use_container_width=True):
    try:
        if advisor_id:
            endpoint = f"{student_endpoint}/advisors/{advisor_id}"
            logger.debug(endpoint)
            response = requests.get(endpoint)
            data = response.json()
            if data:
                st.success("Advisor Results Fetched Successfully!")
                st.json(data) 
            else:
                st.warning("No data found for the given Advisor ID.")
    except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for student {advisor_id}: {e}")
            st.error(f"Failed to fetch advisor results. Please try again later.")
