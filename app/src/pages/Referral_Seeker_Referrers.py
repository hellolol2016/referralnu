import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

API_BASE_URL = "http://web-api:4000/referrers"

# Page title and subtitle
st.title("Referrer Profiles")
st.markdown("""
Explore and search through referrer profiles. View details such as their name, email, number of referrals, and the company they are associated with.
""")

# Add a sidebar with a button to fetch data
st.sidebar.title("Navigation")
fetch_data = st.sidebar.button("Fetch Referrer Profiles")

# Main header
st.header("Referrer Profile Table")

# Add a state variable for the fetched data
if "referrer_data" not in st.session_state:
    st.session_state.referrer_data = None

# Fetch data when the button is clicked
if fetch_data or st.session_state.referrer_data is None:
    with st.spinner("Fetching referrer data..."):
        try:
            response = requests.get(API_BASE_URL)
            if response.status_code == 200:
                st.session_state.referrer_data = response.json()
                st.success("Data fetched successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")

# Check if data is available
if st.session_state.referrer_data:
    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(
        st.session_state.referrer_data,
        columns=["referrerId", "name", "email", "numReferrals", "company_name"]
    )

    # Add filters for company name and number of referrals
    st.subheader("Filters")
    company_filter = st.selectbox("Filter by Company", options=["All"] + df["company_name"].unique().tolist())
    referral_filter = st.slider("Filter by Minimum Referrals", min_value=0, max_value=int(df["numReferrals"].max()), value=0)

    # Apply filters
    if company_filter != "All":
        df = df[df["company_name"] == company_filter]
    df = df[df["numReferrals"] >= referral_filter]

    # Display the filtered DataFrame
    st.success(f"Found {len(df)} profiles matching your filters.")
    st.dataframe(df, use_container_width=True)
