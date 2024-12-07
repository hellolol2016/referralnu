import streamlit as st
import requests

# Back button
if st.button("← Back to Referrer Home"):
    st.switch_page("pages/Referrer_Home.py")

st.title("All Requests")

requests_endpoint = "http://web-api:4000/requests"
student_endpoint = "http://web-api:4000/students"
company_endpoint = "http://web-api:4000/companies"

reqs = []
try:
    reqs = requests.get(requests_endpoint).json()
except Exception as e:
    st.error("Could not connect to API. Using dummy data.")
    reqs = []

# Fetch referrer and student names for each request
for req in reqs:
    try:
        # Fetch student data
        student_response = requests.get(f"{student_endpoint}/{req['studentId']}")
        if student_response.status_code == 200:
            student_data = student_response.json()
            if isinstance(student_data, list) and len(student_data) > 0:
                first_student = student_data[0]
                student_name = f"{first_student.get('firstName', 'Unknown')} {first_student.get('lastName', 'Unknown')}"
            elif isinstance(student_data, dict):
                student_name = f"{student_data.get('firstName', 'Unknown')} {student_data.get('lastName', 'Unknown')}"
            else:
                student_name = "Unknown Student"
        else:
            student_name = "Unknown Student"
    except Exception as e:
        student_name = "Unknown Student"
        st.error(f"Error fetching student data: {str(e)}")

    try:
        # Fetch company data
        company_response = requests.get(f"{company_endpoint}/{req['companyId']}")
        if company_response.status_code == 200:
            company_data = company_response.json()
            if isinstance(company_data, list) and len(company_data) > 0:
                first_company = company_data[0]
                company_name = first_company.get("name", "Unknown company")
            elif isinstance(company_data, dict):
                company_name = company_data.get("name", "Unknown company")
            else:
                company_name = "Unknown company"
        else:
            company_name = "Unknown company"
    except Exception as e:
        company_name = "Unknown company"
        st.error(f"Error fetching company data: {str(e)}")

    req["studentName"] = student_name
    req["companyName"] = company_name

# Create a search bar
search_query = st.text_input("Search requests by company name, student name, or request ID")

# Filter requests based on the search query
filtered_reqs = []
if reqs:
    for req in reqs:
        if (
            search_query.lower() in req.get("companyName", "").lower()
            or search_query.lower() in req.get("studentName", "").lower()
            or search_query.lower() in str(req.get("requestId", "")).lower()
        ):
            filtered_reqs.append(req)

# Display the filtered requests in a table
if filtered_reqs:
    st.subheader("Requests")
    for req in filtered_reqs:
        with st.container():
            st.markdown(f"**Req ID:** {req['requestId']}")
            st.markdown(f"**Company Name:** {req['companyName']}")
            st.markdown(f"**Student Name:** {req['studentName']}")
            st.markdown("---")
else:
    st.write("No requests found.")
