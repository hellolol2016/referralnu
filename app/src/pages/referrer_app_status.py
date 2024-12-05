import streamlit as st
import requests

# Back button
if st.button("← Back to Referrer Home"):
    st.switch_page("pages/Referrer_Home.py")

# Base API URL
BASE_API_URL = "http://web-api:4000/requests"
UPDATE_STATUS_URL = "http://web-api:4000/status"

# Streamlit App Title
st.title("View and Update Request Details by Student ID")

# Input for Student ID
student_id = st.text_input("Enter Student ID")

# Fetch and display request details
if st.button("Fetch Request Details"):
    if not student_id:
        st.warning("Please enter a Student ID.")
    else:
        try:
            # Fetch all requests from the backend
            response = requests.get(BASE_API_URL)

            if response.status_code == 200:
                data = response.json()
                st.subheader("Request Details")

                # Filter requests based on the provided student ID
                filtered_data = [item for item in data if str(item.get("studentId")) == student_id]

                if filtered_data:
                    for item in filtered_data:
                        request_id = item.get("requestId", "N/A")
                        pending_status = item.get("pendingStatus", "Not Available")
                        company_id = item.get("companyId", "Not Available")
                        created_at = item.get("createdAt", "Not Available")

                        # Display current request details
                        st.markdown(f"**Request ID:** {request_id}")
                        st.markdown(f"**Pending Status:** {pending_status}")
                        st.markdown(f"**Company ID:** {company_id}")
                        st.markdown(f"**Created At:** {created_at}")

                        # Use session state to maintain selected status
                        if f"new_status_{request_id}" not in st.session_state:
                            st.session_state[f"new_status_{request_id}"] = pending_status

                        new_status = st.selectbox(
                            f"Update Status for Request ID {request_id}",
                            options=["pending", "accepted", "rejected"],
                            index=["pending", "accepted", "rejected"].index(st.session_state[f"new_status_{request_id}"]),
                            key=f"select_{request_id}"
                        )

                        # Update button for each request
                        if st.button(f"Update Status for Request ID {request_id}", key=f"update_{request_id}"):
                            try:
                                update_payload = {"pendingStatus": new_status}
                                update_response = requests.put(f"{UPDATE_STATUS_URL}/{request_id}", json=update_payload)

                                if update_response.status_code == 200:
                                    st.success(f"Status for Request ID {request_id} updated successfully to '{new_status}'.")
                                    st.session_state[f"new_status_{request_id}"] = new_status
                                    st.experimental_rerun()  # Refresh the page to reflect the updated status
                                else:
                                    st.error(f"Failed to update status for Request ID {request_id}.")
                            except Exception as e:
                                st.error(f"Error updating status for Request ID {request_id}: {str(e)}")
                        st.markdown("---")
                else:
                    st.warning("No requests found for the given Student ID.")
            else:
                st.error(f"Failed to fetch request details. HTTP Status: {response.status_code}")
        except Exception as e:
            st.error(f"Error fetching request details: {str(e)}")
