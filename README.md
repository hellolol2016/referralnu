# Fall 2024 CS 3200 NuReferrals Project Repository
Team Members: Yicheng Wang, Sheryl Cheng, Shireen Kumar, Andreas Seferian, Isha Sakamuri

NUReferrals, aims to tap into one branch of professional networking through referrals. Job seekers, especially students, can easily find and request referrals from industry professionals in their desired fields, significantly enhancing their chances of landing interviews and job offers. In addition, industry professionals can effortlessly discover qualified candidates to fill their referral slots through detailed applicant profiles, streamlining the hiring process. Our app also facilitates connections through industry-hosted events, allowing users to network face-to-face and engage with potential referrers directly.

## Current Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for the data model and data base in the `./database-files` directory


## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them. 
