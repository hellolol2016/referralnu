import streamlit as st
import requests

# Back button
if st.button("← Back to Home"):
    st.switch_page("pages/Referrer_Home.py")

st.title("All Requests")

# API Endpoints
requests_endpoint = "http://web-api:4000/requests"
student_endpoint = "http://web-api:4000/students"
company_endpoint = "http://web-api:4000/companies"

# Fetch requests data
reqs = []
try:
    reqs = requests.get(requests_endpoint).json()
except Exception as e:
    st.error("Could not connect to the API. Please try again later.")
    st.write(e)

# Fetch additional details for requests
for req in reqs:
    try:
        # Get student information
        student_response = requests.get(f"{student_endpoint}/{req['studentId']}")
        student_data = student_response.json()
        student_name = f"{student_data[0].get('firstName', 'Unknown')} {student_data[0].get('lastName', 'Unknown')}"
    except Exception:
        student_name = "Unknown Student"

    try:
        # Get company information
        company_response = requests.get(f"{company_endpoint}/{req['companyId']}")
        company_data = company_response.json()
        company_name = company_data[0].get("name", "Unknown Company")
    except Exception:
        company_name = "Unknown Company"

    # Add fetched details to the request
    req["studentName"] = student_name
    req["companyName"] = company_name

# Search bar
search_query = st.text_input("Search requests by company name, student name, or request ID").lower()

# Filter requests based on the search query
filtered_reqs = [
    req for req in reqs if search_query in req.get("companyName", "").lower()
    or search_query in req.get("studentName", "").lower()
    or search_query in str(req.get("requestId", "")).lower()
]

# Display the filtered requests
if filtered_reqs:
    st.subheader("Requests")
    for req in filtered_reqs:
        with st.container():
            st.markdown(f"**Request ID:** {req['requestId']}")
            st.markdown(f"**Company Name:** {req['companyName']}")
            st.markdown(f"**Student Name:** {req['studentName']}")
            st.markdown("---")
else:
    st.write("No requests found.")
