
import streamlit as st
import requests

# Back button
if st.button("← Back to Referrer Home"):
    st.switch_page("pages/Referrer_Home.py")

st.title("All Requests")

requests_endpoint = "http://web-api:4000/requests"
student_endpoint = "http://web-api:4000/students"
company_endpoint = "http://web-api:4000/companies"


reqs =  []
try:
  reqs = requests.get(requests_endpoint).json()
  #st.write(reqs)
except Exception as e:
  st.write(e)
  st.write("**Important**: Could not connect to api, so using dummy data.")
  connections = [
    ]

# Fetch referrer and student names for each connection
for req in reqs:
    try:
        student_response = requests.get(f"{student_endpoint}/{req['studentId']}")
        student_data = student_response.json()
        #st.write(type(student_data))
        student_name = student_data[0].get("firstName") + " " + student_data[0].get("lastName")
    except Exception as e:
        student_name = "Unknown Student"
    try:
        company_response = requests.get(f"{company_endpoint}/{req['companyId']}")
        company_data = company_response.json()
        #st.write(type(student_data))
        company_name = company_data[0].get("name")
    except Exception as e:
        st.write(e)
        company_name = "Unknown company"

    req["studentName"] = student_name
    req["companyName"] = company_name

# Create a search bar
search_query = st.text_input("Search requests by company name, student name, or request ID")

# Filter connections based on the search query
if reqs:
    filtered_reqs = []
    for req in reqs:
        #st.write(req)
        if (search_query in req.get("companyName", "").lower() or
            search_query in req.get("studentName", "").lower() or
            search_query in str(req.get("requestId", "")).lower()):
            filtered_reqs.append(req)

# Display the filtered connections in a table
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
