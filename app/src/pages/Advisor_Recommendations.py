import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
#from streamlit_modal import Modal

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

referrer_endpoint = "http://web-api:4000/referrers"

st.title(f"Get Best Referrers")
st.write('')
st.write('')
st.write('### Which Method Would You Like to Look For Referrers Through')

#modal = Modal(key="top_referrers_modal")

if st.button('Get top referrers', type='primary', use_container_width=True):
    try:
        endpoint = f"{referrer_endpoint}/top"
        logger.debug(endpoint)
        response = requests.get(endpoint)
        data = response.json()
        if data:
            st.success("Results Fetched Successfully!")
            st.json(data) 
        else:
            st.warning("No data found for the given Student ID.")
    except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for top referrers: {e}")
            st.error(f"Failed to fetch student results. Please try again later.")

# maybe we could make a modal that shows this information?
#if st.button('Get top referrers', type='primary', use_container_width=True):
# try:
#      endpoint = f"{referrer_endpoint}/top"
#      response = requests.get(endpoint)
#      data = response.json()
#      if data:
#           st.success("Results Fetched Successfully!")
#           if st.button("View Top Referrers"):
#             modal.open()
#           # st.json(data) 
#           if modal.is_open():
#             with modal.container():
#                 st.header("Top Referrers")
#                 for referrer in data:
#                     st.subheader(f"Referrer: {referrer['name']}")
#                     st.text(f"ID: {referrer['referrerId']}")
#                     st.text(f"Company: {referrer['company_name']}")
#                     st.text(f"Referrals: {referrer['numReferrals']}")
#                     st.divider()
#      else:
#           st.warning("No data found for the given Student ID.")
# except requests.exceptions.RequestException as e:
#      logger.error(f"Error fetching data for top referrers: {e}")
#      st.error(f"Failed to fetch student results. Please try again later.")

if st.button('Referrers with the Most Referrals Left to Give', type='primary', use_container_width=True):
     st.switch_page("pages/Advisor_Recommendations_Left.py")