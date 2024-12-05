import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Advisor Homepage')

if st.button('Get Student Information', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Student_Info.py")

if st.button('Track Student Referral Progress', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Referral_Progress.py")

if st.button('Track Advisor Results', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Results.py")

if st.button('Find Best Referral Givers', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Recommendations.py")

if st.button('Message Students', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_followup.py")