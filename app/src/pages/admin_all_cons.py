import streamlit as st
import requests

st.title("All Connections")

connections_endpoint = "http://web-api:4000/connections"
referrer_endpoint = "http://web-api:4000/referrers"
student_endpoint = "http://web-api:4000/students"


connections =  []
try:
  connections = requests.get(connections_endpoint).json()
except Exception as e:
  st.write(e)
  st.write("**Important**: Could not connect to api, so using dummy data.")
  connections = [
        {"connectionId": 1, "referrerId": 1, "studentId": 1},
        {"connectionId": 2, "referrerId": 2, "studentId": 2}
    ]

# Fetch referrer and student names for each connection
for connection in connections:
    try:
        referrer_response = requests.get(f"{referrer_endpoint}/{connection['referrerId']}")
        referrer_name = referrer_response.json().get("name", "Unknown Referrer")
    except Exception as e:
        st.write(e)
        referrer_name = "Unknown Referrer"

    try:
        student_response = requests.get(f"{student_endpoint}/{connection['studentId']}")
        student_name = student_response.json().get("name", "Unknown Student")
    except Exception as e:
        student_name = "Unknown Student"

    connection["referrerName"] = referrer_name
    connection["studentName"] = student_name

# Display the connections in a table
if connections:
    st.subheader("Connections")
    for connection in connections:
        with st.container():
            st.markdown(f"**Connection ID:** {connection['connectionId']}")
            st.markdown(f"**Referrer Name:** {connection['referrerName']}")
            st.markdown(f"**Student Name:** {connection['studentName']}")
            st.markdown("---")
else:
    st.write("No connections found.")
