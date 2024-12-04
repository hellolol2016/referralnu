import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Advisor Homepage')

student_endpoint = "http://localhost:4000/students"

student_id = st.text_input("Enter Student ID to fetch results:")

if st.button('Get Student information', type='primary', use_container_width=True):
    try:
        if student_id:
            endpoint = f"{student_endpoint}/{student_id}"
            logger.debug(endpoint)
            response = requests.get(endpoint)
            data = response.json()
            if data:
                st.success("Student Results Fetched Successfully!")
                st.json(data) 
            else:
                st.warning("No data found for the given Student ID.")
    except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for student {student_id}: {e}")
            st.error(f"Failed to fetch student results. Please try again later.")