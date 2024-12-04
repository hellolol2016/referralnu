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

# 4.1
if st.button('See Resume Information',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer/all_resumes.py')

# 4.2
if st.button('Remove Companies',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer/remove_company.py')

# 4.3
if st.button("Change Application Status",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer/app_status.py')

# 4.4
if st.button("Communicate Requirements",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer/con.py')

# 4.5
if st.button("Student Referral Status",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer/student_status.py')

# 4.6
if st.button("Edit Contact Information",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/referrer/info.py')