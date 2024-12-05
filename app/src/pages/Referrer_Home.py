import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Referrer Giver Page')

st.write('')
st.write('')
st.write('### What would you like to do?')

if st.button('See All Requests',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer_all_reqs.py')

# 4.1, 4.4
if st.button('See Student Information',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer_all_resumes.py')

# 4.2
if st.button('Manage Companies',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer_remove_company.py')

# 4.3, 4.5
if st.button("View and Change Application Status",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer_app_status.py')


# 4.6
if st.button("Edit Contact Information",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer_info.py')