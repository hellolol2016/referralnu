import streamlit as st
import requests
# Back button
if st.button("← Back to Admin Home"):
    st.switch_page("pages/admin_home.py")

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
        referrer_response.raise_for_status()
        referrer_data = referrer_response.json()
        if isinstance(referrer_data, list) and len(referrer_data) > 0:
            referrer_name = referrer_data[0].get("name", "Unknown Referrer")
        elif isinstance(referrer_data, dict):
            referrer_name = referrer_data.get("name", "Unknown Referrer")
        #st.write(type(referrer_data))  # Debug: Print the response to see its structure
        #st.write(referrer_data[0].get("name"))  # Debug: Print the response to see its structure
        referrer_name = referrer_data[0].get("name", "Unknown Referrer") 
    except Exception as e:
        st.write(e)
        referrer_name = "Unknown Referrer"

    try:
        student_response = requests.get(f"{student_endpoint}/{connection['studentId']}")
        student_data = student_response.json()
        #st.write(type(student_data))  # Debug: Print the response to see its structure
        student_name = student_data[0].get("firstName") + " " + student_data[0].get("lastName")
    except Exception as e:
        student_name = "Unknown Student"

    connection["referrerName"] = referrer_name
    connection["studentName"] = student_name

# Create a search bar
search_query = st.text_input("Search connections by referrer name, student name, or connection ID")

# Filter connections based on the search query
if connections:
    filtered_connections = []
    for connection in connections:
        if (search_query.lower() in connection["referrerName"].lower() or
            search_query.lower() in connection["studentName"].lower() or
            search_query.lower() in str(connection["connectionId"]).lower()):
            filtered_connections.append(connection)

# Display the filtered connections in a table
if filtered_connections:
    st.subheader("Connections")
    for connection in filtered_connections:
        with st.container():
            st.markdown(f"**Connection ID:** {connection['connectionId']}")
            st.markdown(f"**Referrer Name:** {connection['referrerName']}")
            st.markdown(f"**Student Name:** {connection['studentName']}")
            if st.button(f"View Messages for Connection {connection['connectionId']}", key=connection['connectionId']):
                st.session_state["message_connectionId"]= connection['connectionId']
                st.session_state["message_studentName"] = connection['studentName']
                st.session_state["message_referrerName"] = connection['referrerName']
                #st.query_params["connectionId"] = connection['connectionId']
                st.switch_page("pages/conversation.py")
            if st.button("Delete Connection", key=("delete", connection['connectionId'])):
                requests.delete(f"{connections_endpoint}/{connection['connectionId']}")
                st.rerun()
            st.markdown("---")
else:
    st.write("No connections found.")
