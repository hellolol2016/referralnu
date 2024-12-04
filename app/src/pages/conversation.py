import streamlit as st
import requests
connectionId = st.session_state["message_connectionId"]
referrerName = st.session_state["message_referrerName"]
studentName = st.session_state["message_studentName"]

st.title(f"Conversation between { studentName } and { referrerName }")
#connectionId = st.query_params.get("connectionId", None)[0]

messages_endpoint = "http://web-api:4000/messages"
referrer_endpoint = "http://web-api:4000/referrers"
student_endpoint = "http://web-api:4000/students"


messages =  []
try:
    response = requests.get(f"{messages_endpoint}/conversation/{connectionId}")
    response.raise_for_status()  # Check for HTTP errors
    messages = response.json()
except Exception as e:
  st.write(e)
  st.write("**Important**: Could not connect to api, so using dummy data.")
  messagses = [
    ]
# Display messages
if messages:
    for message in messages:
        with st.container():
          if message.get('studentSent', False):
            st.markdown(f"**From:** {studentName}")
          else:
            st.markdown(f"**From:** {referrerName}")
          st.markdown(f"**Message:** {message.get('messageContent', 'No content')}")
          st.markdown(f"**Sent At:** {message.get('sentAt', 'Unknown time')}")
          st.markdown("---")
else:
    st.write("No messages found for this conversation")
