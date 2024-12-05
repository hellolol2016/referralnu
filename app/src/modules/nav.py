# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")
    st.sidebar.page_link("Home.py", label = "Home", icon = "🏠")




#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/admin_home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link("pages/admin_all_cons.py", label = "All Connections")
    st.sidebar.page_link("pages/admin_all_reqs.py", label = "All Requests")
    st.sidebar.page_link("pages/admin_manage_connections.py", label = "Manage Connections")
    st.sidebar.page_link("pages/admin_student_messages", label = "Student Messages")

def AdvisorPageNav():
    st.sidebar.page_link("pages/31_Advisor_Home.py", label = "Advisor")
    st.sidebar.page_link("pages/Advisor_Recommendations.py", label = "Recommendations")
    st.sidebar.page_link("pages/Advisor_Referral_Progress.py", label = "Progress")
    st.sidebar.page_link("pages/Advisor_Results.py", label = "Results")
    st.sidebar.page_link("pages/Advisor_Student_Info.py", label = "Student Info")


def ReferralSeekerPageNav():
    st.sidebar.page_link("pages/Referral_Seeker.py", label = "Referral Seeker")
    st.sidebar.page_link("pages/Referral_Seeker_Requests.py", label = "Requests")
    st.sidebar.page_link("pages/Referral_Seeker_Search_Connections.py", label = "Connections")

def ReferrerPageNav():
    st.sidebar.page_link("pages/Referrer_Home.py", label = "Referrer")
    st.sidebar.page_link("pages/referrer_remove_company.py", label = "Change Employment")
    st.sidebar.page_link("pages/referrer_all_resumes.py", label = "Resumes")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks():
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:


        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
        
        if st.session_state["role"] == "advisor":
            AdvisorPageNav()

        if st.session_state["role"] == "referrer":
            ReferrerPageNav()
        
        if st.session_state["role"] == "Referral Seeker":
            ReferralSeekerPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
