import streamlit as st

# Fetch query parameters using st.query_params
query_params = st.query_params
referrer_id = query_params.get("referrer_id")

# Title for the messaging page
st.title("Send Message")

if referrer_id:
    st.markdown(f"### Sending Message to Referrer ID: {referrer_id}")
else:
    st.error("No Referrer ID provided. Please go back and try again.")

# Input for the message content
message = st.text_area("Enter your message here", height=200)

# Button to simulate sending the message
if st.button("Send Message"):
    if message and referrer_id:
        st.success(f"Your message has been sent to Referrer ID {referrer_id}!")
        st.write(f"**Message Sent:**\n{message}")
    else:
        st.error("Please make sure to enter a message before sending.")
