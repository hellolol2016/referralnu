import streamlit as st
import requests

# Back button
if st.button("← Back to Home"):
    st.switch_page("pages/Referrer_Home.py")

st.title("Manage Companies")

# API Endpoint
companies_endpoint = "http://web-api:4000/companies"

# Store locally "deleted" companies
if "deleted_companies" not in st.session_state:
    st.session_state.deleted_companies = set()

# Search bar for company ID
company_id_query = st.text_input("Search company by ID")

# If a company ID is provided, fetch and display the company information
if company_id_query:
    try:
        # Fetch company information
        response = requests.get(f"{companies_endpoint}/{company_id_query}")

        # Check for valid response
        if response.status_code == 200:
            company_data = response.json()

            # Handle case where API returns a list
            if isinstance(company_data, list) and company_data:
                company = company_data[0]  # Access the first item in the list
            elif isinstance(company_data, dict):
                company = company_data
            else:
                st.warning("Invalid response format from the server.")
                company = None

            if company:
                # Check if the company is in the deleted list
                if str(company.get("companyId")) in st.session_state.deleted_companies:
                    st.warning("This company has been removed from the page.")
                else:
                    # Display company details
                    st.subheader("Company Information")
                    st.markdown(f"**Company ID:** {company.get('companyId', 'N/A')}")
                    st.markdown(f"**Company Name:** {company.get('name', 'N/A')}")

                    # Remove company button
                    if st.button("Remove Company", key=f"remove_{company.get('companyId')}"):
                        st.session_state.deleted_companies.add(str(company.get("companyId")))
                        st.success("Company removed from the page.")
            else:
                st.warning("No valid company data found.")
        elif response.status_code == 404:
            st.warning("Company not found.")
        else:
            st.error(f"Failed to fetch company information: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error(f"Error while fetching company information: {str(e)}")
else:
    st.write("Enter a Company ID to search.")
