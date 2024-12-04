import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Admin, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View All Requests', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/admin/all_reqs.py')

if st.button('Manage Connections / Conversations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/admin/all_cons.py')

if st.button('Contact Student', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/admin/student_messages.py')

if st.button('Remove user', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/admin/remove_student.py')