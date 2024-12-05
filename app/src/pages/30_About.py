import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About ReferralNU")

st.markdown (
    """
        Did you know that an estimated 70-80% of all jobs are never posted? That hidden job market can only be 
    reached through connections; experts suggest that around 80% of jobs are filled through networking (Forbes). 
    Our app, NUReferrals, aims to tap into one branch of professional networking through referrals. Job 
    seekers, especially students, can easily find and request referrals from industry professionals in their 
    desired fields, significantly enhancing their chances of landing interviews and job offers. In addition, 
    industry professionals can effortlessly discover qualified candidates to fill their referral slots 
    through detailed applicant profiles, streamlining the hiring process.
    
        ReferralsNU requires existing data on users and referrals to function meaningfully, and it generates 
    new data with each interaction. This allows job seekers to leverage connections that can be tracked, 
    analyzed, and managed over time for the best networking and employment outcomes. Our app also ensures 
    that all interactions are safe and authentic through administrator verification. They can quickly verify 
    user profiles, monitor referral activities, and facilitate effective communication about platform policies, 
    ensuring that all members adhere to community standards. Co-op advisors can track student progress and 
    facilitate networking opportunities, offering personalized guidance and networking opportunities tailored 
    to individual users’ career goals.
    """
        )
