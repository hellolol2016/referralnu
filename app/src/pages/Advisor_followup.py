import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

advisor_endpoint = "http://web-api:4000/advisors/set_reminder"

st.title(f"Message Student")

advisor_id = st.text_input("Enter Advisor ID:")
student_id = st.text_input("Enter Student ID:")
message = st.text_area("Enter Message:")
follow_up_days = st.number_input("Follow-Up Days (optional, default 3 days):", min_value=1, value=3)

if st.button('Get Follow-up Date', type='primary', use_container_width=True):
    if not advisor_id or not student_id or not message:
        st.error("Please provide all required fields: Advisor ID, Student ID, and Message.")
    else:
        parameters = {
            "studentId": int(student_id),
            "advisorId": int(advisor_id),
            "content": message,
            "followUpDays": int(follow_up_days)
        }
    try:
        response = requests.post(f"{advisor_endpoint}/{student_id}/{advisor_id}", json=parameters)
        if response.status_code == 201:
            data = response.json()
            st.success(f"Reminder set successfully! Follow-Up Date: {data.get('followUpDate')}")
        else:
            error_message = response.json().get('error', 'An error occurred.')
            st.error(f"Failed to set reminder: {error_message}")
    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to the server. Please try again later.")