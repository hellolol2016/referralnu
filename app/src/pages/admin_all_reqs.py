import streamlit as st
import requests

# Back button
if st.button("← Back to Home"):
    st.switch_page("home")

st.title("All Companies")

# API Endpoints
companies_endpoint = "http://web-api:4000/companies"

# Fetch all companies
companies = []
try:
    response = requests.get(companies_endpoint)
    response.raise_for_status()  # Check for HTTP errors
    companies = response.json()
except Exception as e:
    st.write(e)
    st.error("**Important**: Could not connect to the API. Please try again later.")
    companies = []

# Create a search bar
search_query = st.text_input("Search companies by name or company ID").lower()

# Filter companies based on the search query
filtered_companies = []
if companies:
    for company in companies:
        if (search_query in company.get("name", "").lower() or
            search_query in str(company.get("companyId", "")).lower()):
            filtered_companies.append(company)

# Display the filtered companies in a table
if filtered_companies:
    st.subheader("Companies")
    for company in filtered_companies:
        with st.container():
            st.markdown(f"**Company ID:** {company['companyId']}")
            st.markdown(f"**Company Name:** {company['name']}")
            st.markdown("---")
else:
    st.write("No companies found.")
