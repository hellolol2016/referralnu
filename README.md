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

## API Endpoints
There are several api endpoints that were created which allows for each persona (referrers, students, co-op advisors, and admins) to fulfill certain actions. These endpoints are organized into seven main routes: referrers, advisors, companies, connections, messages, requests, and students. These routes all relate to the entities that require the most functionality. Each route supports various HTTP methods, including GET, POST, PUT, and DELETE, allowing users to retrieve, create, update, and delete data as needed. For example, co-op advisors need to be able to search for certain students's progress to keep track on them. This task uses the API in students that uses a GET request to get student information from the database.
