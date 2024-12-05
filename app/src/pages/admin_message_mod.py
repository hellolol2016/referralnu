
import streamlit as st
import requests
# Back button
if st.button("← Back to Admin Home"):
    st.switch_page("pages/admin_home.py")

st.title(f"Message filter and delete")
#connectionId = st.query_params.get("connectionId", None)[0]

messages_endpoint = "http://web-api:4000/messages"
referrer_endpoint = "http://web-api:4000/referrers"
student_endpoint = "http://web-api:4000/students"


messages =  []
try:
    response = requests.get(f"{messages_endpoint}")
    response.raise_for_status()  # Check for HTTP errors
    messages = response.json()
except Exception as e:
  st.write(e)
  st.write("**Important**: Could not connect to api, so using dummy data.")
  messagses = [
    ]

search_query = st.text_input("Search messages by content")

# Filter connections based on the search query
if messages:
    filtered_mes= []
    for message in messages:
        #st.write(req)
        if (search_query in message.get("messageContent", "").lower() or
            search_query in message.get("studentName", "").lower()):
            filtered_mes.append(message)


# Display messages
if filtered_mes:
    for message in filtered_mes:
        with st.container():
          if message.get('studentSent', False):
            try:
                student_response = requests.get(f"{student_endpoint}/{message['studentId']}")
                student_data = student_response.json()
                #st.write(type(student_data))  # Debug: Print the response to see its structure
                student_name = student_data[0].get("firstName") + " " + student_data[0].get("lastName")
            except Exception as e:
                student_name = "unknown student"

            st.markdown(f"**{student_name}** - {message.get('sentAt', 'Unknown time')}")
          else:
            try:
                referrer_response = requests.get(f"{referrer_endpoint}/{message['referrerId']}")
                referrer_data = referrer_response.json()
                #st.write(type(student_data))  # Debug: Print the response to see its structure
                referrer_name = referrer_data[0].get("name")
            except Exception as e:
                referrer_name = "unknown referrer"
            st.markdown(f"**From:** {referrer_name}")
          st.write(f"{message.get('messageContent', 'No content')}")
          #st.markdown(f"**Sent At:** {message.get('sentAt', 'Unknown time')}")
          st.markdown("---")
else:
    st.write("No messages found for this conversation")
