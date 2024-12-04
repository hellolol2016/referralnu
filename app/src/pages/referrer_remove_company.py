# 4.2

import logging
import streamlit as st
import requests

# Base API URL
BASE_API_URL = "http://web-api:4000/referrer"

# Configure logger
logger = logging.getLogger(__name__)

# Streamlit App Title
st.title("Manage Referrer's Company List")

# Function to include a company for referrals
def include_company(referrer_id, company_id):
    payload = {"action": "include", "companyId": company_id}
    try:
        response = requests.put(f"{BASE_API_URL}/{referrer_id}/companies", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to include company: {response.status_code}")
            st.write(response.text)
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Function to remove a company from referrals
def remove_company(referrer_id, company_id):
    payload = {"action": "remove", "companyId": company_id}
    try:
        response = requests.put(f"{BASE_API_URL}/{referrer_id}/companies", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to remove company: {response.status_code}")
            st.write(response.text)
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Inputs for referrer and company details
referrer_id = st.text_input("Enter Referrer ID")
company_id = st.text_input("Enter Company ID")

# Include company button
if st.button("Include Company"):
    if not referrer_id or not company_id:
        st.warning("Referrer ID and Company ID are required to include a company.")
    else:
        result = include_company(referrer_id, company_id)
        if result:
            st.success("Company included successfully!")
            st.json(result)

# Remove company button
if st.button("Remove Company"):
    if not referrer_id or not company_id:
        st.warning("Referrer ID and Company ID are required to remove a company.")
    else:
        result = remove_company(referrer_id, company_id)
        if result:
            st.success("Company removed successfully!")
            st.json(result)
