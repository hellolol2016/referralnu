import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Referral Seeker, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# 2.1
if st.button('Search For Connections',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Referral_Seeker_Search_Connections.py')

#2.2, 2.3, 2.4
if st.button('Request and Track Referrals',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Referral_Seeker_Requests.py')

# 2.5
if st.button("Find Referrers",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Referral_Seeker_Referrers.py')

#2.6
if st.button("Seek Guidance From Advisor",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Referral_Seeker_Advisor.py')