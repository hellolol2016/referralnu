import pandas as pd
import streamlit as st
import requests

API_URL = "http://web-api:4000/connections"

st.title("Connections Viewer")


# Function to fetch connections by studentId
def fetch_connections(student_id):
    try:
        response = requests.get(f"{API_URL}/{student_id}")
        if response.status_code == 200:
            return response.json()  
        else:
            st.error(f"Failed to fetch connections: {response.status_code}")
            st.write(response.text)
            return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


# Input for student ID
student_id = st.text_input("Enter Student ID")

if student_id:
    if st.button("Load Connections"):
        connections = fetch_connections(student_id)
        if connections:
            st.success("Connections loaded successfully!")

          
            df = pd.DataFrame(connections)


            required_columns = ["connectionId", "creationDate", "referrerId", "studentId"]
            if all(col in df.columns for col in required_columns):
                df["Send Message"] = df["referrerId"].apply(
                    lambda ref_id: f'<a href="/Referral_Seeker_Referrer_Messages?referrer_id={ref_id}" target="_self">Send Message</a>'
                )

                df_display = df[["connectionId", "creationDate", "referrerId", "studentId", "Send Message"]]
                st.markdown(
                    df_display.to_html(escape=False, index=False),
                    unsafe_allow_html=True
                )
            else:
                st.error(f"The response does not contain the required columns: {required_columns}")
        else:
            st.warning("No connections found.")
else:
    st.warning("Please enter a Student ID.")
