import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

student_endpoint = "http://web-api:4000/students"

st.title(f"Get Student Progress")
st.write('')
st.write('')
st.write('### Which Student would you like information on?')

student_id = st.text_input("Enter Student ID to fetch results:")

if st.button('Get Student Progress', type='primary', use_container_width=True):
    try:
        if student_id:
            endpoint = f"{student_endpoint}/{student_id}/results"
            logger.debug(endpoint)
            response = requests.get(endpoint)
            data = response.json()
            if data:
                st.success("Student Results Fetched Successfully!")
                df = pd.DataFrame(data)
                st.subheader("Advisor Information:")
                st.table(df)
            else:
                st.warning("No data found for the given Student ID.")
    except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for student {student_id}: {e}")
            st.error(f"Failed to fetch student results. Please try again later.")
