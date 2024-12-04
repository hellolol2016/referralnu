import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

student_endpoint = "http://web-api:4000/students"

st.title(f"Get Best Referrers")
st.write('')
st.write('')
st.write('### Which Method Would You Like to Look For Referrers Through')


if st.button('Referrers that Give the Most Referrals', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Recommendations_Referrer.py")

if st.button('Referrers with the Most Referrals Left to Give', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Recommendations_Left.py")