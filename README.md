# NUReferrals

> **Project Description**  
NUReferrals, aims to tap into one branch of professional networking through referrals. Job seekers, especially students, can easily find and request referrals from industry professionals in their desired fields, significantly enhancing their chances of landing interviews and job offers. In addition, industry professionals can effortlessly discover qualified candidates to fill their referral slots through detailed applicant profiles, streamlining the hiring process. Our app also facilitates connections through industry-hosted events, allowing users to network face-to-face and engage with potential referrers directly.
---

## **Table of Contents**

1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Setup and Installation](#setup-and-installation)  
5. [Running the Project](#running-the-project)  
6. [Environment Variables & Secrets](#environment-variables--secrets)  
7. [Contributing](#contributing)  
8. [Team Members](#team-members)  
9. [License](#license)

---

## **Introduction**

**Why does this project exist?**  

Did you know that an estimated 70-80% of all jobs are never posted? That hidden job market can only be reached through connections; experts suggest that around 80% of jobs are filled through networking (Forbes). Our app, NUReferrals, aims to tap into one branch of professional networking through referrals. Job seekers, especially students, can easily find and request referrals from industry professionals in their desired fields, significantly enhancing their chances of landing interviews and job offers. In addition, industry professionals can effortlessly discover qualified candidates to fill their referral slots through detailed applicant profiles, streamlining the hiring process. Our app also facilitates connections through industry-hosted events, allowing users to network face-to-face and engage with potential referrers directly.
	
ReferralsNU requires existing data on users and referrals to function meaningfully, and it generates new data with each interaction. This allows job seekers to leverage connections that can be tracked, analyzed, and managed over time for the best networking and employment outcomes. Our app also ensures that all interactions are safe and authentic through administrator verification. They can quickly verify user profiles, monitor referral activities, and facilitate effective communication about platform policies, ensuring that all members adhere to community standards. Co-op advisors can track student progress and facilitate networking opportunities, offering personalized guidance and networking opportunities tailored to individual users’ career goals.

---

## **Features**

There are 4 personas, or people that you can act as, when using NUReferrals

### Administrator
As an administrator, you can… 

### Referral Seeker/ Student
As a referral seeker, you can search through your connections and reach out to referrers. Referral seekers are also able to view, update, and create their own requests and search through referrer profiles with filtering functionality to request referrals from. If students need guidance, they are also able to find advisor contact info in order to reach out.


### Co-op advisor
As a co-op advisor, you need to be able to keep tabs on your students and their progress to make sure that they are on the right track. With that advisors are able to view student information given a student id, advisors can also view students requests and how many are pending, accepted, or rejected. Advisors are also tasked with helping students find the best referrers and companies for students to have the best chance at receiving a referral, with that advisors are able to view the top companies that give out the most referrals and they can view individual referrers who haven’t given out many referrals. Advisor can also message a student and set a follow up date to make sure they are progressing.

### Referral Giver
As a referral giver, you can…

---

## **Tech Stack**

| **Technology**    | **Version** |  
|--------------------|-------------|  
| Programming Language | Python 3.9 |  
| Framework          | Streamlit & Flask |  
| Database           | mySQL |  
| Containerization   | Docker |  

---

## **Setup and Installation**

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/your-username/your-project.git
   cd your-project
   ```

2. **Install Dependencies:**  
   Follow specific commands to install required dependencies.  
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables:**  
   Refer to [Environment Variables & Secrets](#environment-variables--secrets).

---

## **Running the Project**

### **Using Docker**
1. **Build the Docker Image:**  
   ```bash
   docker-compose build
   ```

2. **Run the Containers:**  
   ```bash
   docker compose up -d
   ```

3. **Access the Application:**  
   Visit `http://localhost:8501` in your browser.

---

## **Environment Variables & Secrets**

### **Required Secrets**
List all required secrets and their purposes.

| **Key**            | **Description**              | **Example**          |  
|--------------------|-----------------------------|----------------------|  
| `DB_PASSWORD`      | Database password            | `your_db_password`   |  
| `SECRET_KEY`       | Application secret key       | `random-string`      |  

### **How to Set Secrets:**
1. Create a `.env` file at the root of the project.
2. Add your environment variables:
   ```env
   DB_PASSWORD=your_db_password
   SECRET_KEY=random-string
   ```

---

## **Contributing**

1. Fork the repository.  
2. Create a new feature branch:  
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes:  
   ```bash
   git commit -m "Added a new feature"
   ```
4. Push the branch:  
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## **Team Members**

| **Name**          | **Email**               |  
|--------------------|------------------------|  
| Shireen Kumar      | kumar.shire@northeastern.edu  |  
| Sheryl Cheng       | cheng.sher@northeastern.edu   |  
| Isha Sakamuri      | sakamuri.i@northeastern.edu   |  
| Yicheng Wang       | wang.yicheng4@northeastern.edu|  
| Andreas Seferian   | seferian.a@northeastern.edu   |  

---

## **License**

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## **Contact**

For questions or issues, reach out to Database Dream Team at:  
- Email: team@example.com  
- GitHub Issues: [GitHub Issues Page](https://github.com/hellolol2016/referralnu)

--- 

