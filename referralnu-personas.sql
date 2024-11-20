USE referralnu;

-- User Persona 1: Admin

-- Story 1: As an administrator, I need to be able to verify that referral offers are from real employees so that the app doesn’t get fake referral offers.

SELECT ref.name, ref.company FROM Requests req
JOIN Referrer ref ON req.referrerId = ref.referrerId;

-- Story 2: As an administrator, I need to be able to cut connections that are not considered appropriate and productive to ensure students’ referral searches are as smooth as possible
-- First we want to find all the messages that contain bad words, then we want to delete the connections that are associated with those messages.
SELECT m.message, m.studentId
FROM Messages m
WHERE m.Message LIKE '%BAD WORD HERE%'

DELETE FROM Connections
WHERE connectionId = m.connectionId;
-- Story 3: As an administrator, I need to be able to verify that requests are being seen and accessed so that referral seekers don’t need to wait long times for responses
-- We have a viewCount and lastViewed column in the Requests table that we can use to see how many times a request has been viewed and when it was last viewed.
SELECT viewCount, lastViewed from Requests;
-- Story 4: As an administrator, I need to be able to ensure that referral givers give the referral to the student they said they would so that the process’ integrity is conserved
-- To do this, we can check the status of the connection, and check the message history between the two parties
-- Assume we are looking at student 1 and referrer 1

-- Connections doesn't have a status rn. Maybe request instead?
SELECT c.status, m.message
FROM Connections c
JOIN Messages m ON c.connectionId = m.connectionId
WHERE c.studentId = 1 AND c.referrerId = 1;
-- Story 5: As an administrator, I need to be able to remove or add referral seekers and givers so that people who break the rules are removed from the app.
-- We can do this by deleting the student 1 from Student table, and deleting the referrer 1 from Referrer table
DELETE FROM Students WHERE studentId = 1;
DELETE FROM Referrer WHERE referrerId = 1;
-- Story 6: As an administrator, I need to be able to communicate to users that they are breaking the rules and what the rules are so that no one complains about being removed without a reason.
-- We can do this by sending a message to the user that is breaking the rules, getting their personal contact information and sending a message.
SELECT email from Referrer WHERE referrerId = 1;
SELECT email from Students WHERE studentId = 1;


-- User persona 2: Referral Seeker

-- Story 1: As a referral seeker, I need to be able to search for connections at specific companies so that I can strengthen my application with a trusted recommendation.
SELECT c.connectionId FROM Connections c
JOIN Student stu ON stu.studentId = c.studentId
WHERE LOWER(c.companyName) = LOWER('Company Name');

-- Story 2: As a referral seeker, I need to be able to request referrals from professionals within my target companies so that I can improve my chances of securing an interview.
INSERT INTO Requests (studentId, industryId, companyName, pendingStatus, requestDate)
SELECT stu.studentId, request.industryId, request.company, 'Pending', CURRENT_TIMESTAMP FROM Students stu
JOIN Connections c ON stu.studentId = c.studentId
JOIN Referrer referr ON c.referrerId = referr.referrerId
WHERE referr.company = 'target company';

-- Story 3: As a referral seeker, I need to be able to track the status of my referral requests so that I can stay informed and follow up as needed.
SELECT req.status FROM Requests req 
JOIN Student.stu ON req.studentId = stu.studentId;
where stu.studentId = 1

-- Story 4: As a referral seeker, I need to be able to view a history of my past referral requests, including their status and associated messages, so that I can track my progress and learn from previous interactions.
SELECT Req.requestId, Req.companyName, Req.pendingStatus, Req.requestDate, Req.createdAt, Req.lastViewed, Indus.name, Mes.messageContent, Mes.sentAt
FROM Requests Req
LEFT JOIN Messages Mes ON Req.studentId = M.studentId AND Req.requestId = Mess.connectionId
JOIN Industries Indus ON Req.industryId = Indus.industryId
ORDER BY Req.requestDate DESC;

-- Story 5: As a referral seeker, I need to be able to access profiles of potential referrers with their professional background and availability so that I can approach the most relevant contacts.
SELECT r.referrerId, r.name, r.email, r.phoneNumber, r.company  i.name, c.creationDate 
FROM Students stu
JOIN Connections c ON stu.studentId = c.studentId
JOIN Referrer r ON c.referrerId = r.referrerId
JOIN Industries i ON r.industryId = i.industryId
ORDER BY r.company ASC;

-- Story 6: As a referral seeker, I need to be able to receive guidance on how to request and approach referrals so that I can maximize my chances.
SELECT a.advisorID,a.firstName, a.lastName, a.email, a.phoneNumber
FROM Students s
JOIN Advisor a ON s.advisorId = a.advisorID;
where a.advisorId = 1

-- User Persona 3: Advisor

-- Story 3.1 As an advisor, I need to monitor students' progress in their job search, specifically their application statuses and networking activities.
SELECT s.StudentId, s.firstName, s.lastName, r.createdAt, r.pendingStatus
FROM Students s JOIN Advisor a ON s.advisorId = a.advisorId 
JOIN Requests r ON s.StudentId = r.StudentId
WHERE studentId = 1

-- Story 3.2 As a co-op advisor, I need to be able to view a dashboard of all my students’ application statuses so I can identify who is making progress and who needs assistance.
--
SELECT s.studentId, 
       SUM(req.pendingStatus = 'Pending') AS pendingRequests,
       SUM(req.pendingStatus = 'Accepted') AS acceptedRequests,
       SUM(req.pendingStatus = 'Rejected') AS rejectedRequests
FROM Students s
LEFT JOIN Requests req ON s.studentId = req.studentId
where s.advisorId = 1
GROUP BY s.studentId



-- Story 3.3 As a co-op advisor, I need to be able to communicate directly with students through the app so that I can provide timely feedback and guidance.

SELECT firstName, lastName, email, phoneNumber 
FROM Students
WHERE studentId = 1
-- Story 3.4 As a co-op advisor, I need to be able to set reminders for follow-up communications with students based on their application timelines so that I can make sure they stay on track.

SELECT firstName, lastName, email, phoneNumber 
FROM Students
WHERE studentId = 1

-- Story 3.5 As a co-op advisor, I need to be able to add referral givers that I know to the app so that the referral seekers have as many options as possible.

INSERT INTO Referrer (name, email, phoneNumber, company, adminId, industryId, numReferrals)

-- Story 3.6 As a co-op advisor, I could refer students to connect with certain companies based on data visualizations that show what companies give the most referrals
SELECT referrerId
FROM Referrer
WHERE companyName = (
    SELECT companyName
    FROM Referrer
    GROUP BY companyName
    ORDER BY SUM(numReferrals) DESC
    LIMIT 1
);
SELECT r.referrerId
FROM Referrer r
WHERE r.companyName = (
    SELECT req.companyName
    FROM Requests req
    WHERE req.pendingStatus = 'Accepted'
    GROUP BY req.companyName
    ORDER BY COUNT(req.requestId) DESC
    LIMIT 1
);
--this works by industry for the company with the most accepted requests
-- when it should maybe work by company, which both requests and referrers has, but wouldn't match our ER diagram

-- User Persona 4: Referrer

-- Story 4.1 As a person giving out referrals, I need to be able to see the resumes and skills of people requesting referrals so that I don’t waste any referral slots.
SELECT S.studentId, S.name AS studentName, S.contactInfo AS studentContact, R.company AS referredCompany, C.creationDate AS referralDate
FROM Connections C
JOIN Referrer R ON C.referrerId = R.referrerId
JOIN Students S ON C.studentId = S.studentId

-- Story 4.2 As a person giving out referrals, I need to be able to include or remove the companies I can give referrals to so that I get requests from relevant job seekers.
-- Add a company for a referrer (ex. referrerId = 100)
UPDATE Referrer
SET company = 'Company 2'
WHERE referrerId = 100;

-- Remove a company from the list (set it to NULL)
UPDATE Referrer
SET company = NULL
WHERE referrerId = 100;

-- Story 4.3 As a person giving out referrals, I need to be able to reject or accept applications for referrals so that I can indicate who I will be giving a referral to.
-- Accept an application
UPDATE Requests
SET status = 'Accepted'
-- Reject an application
UPDATE Requests
SET status = 'Rejected'

-- Story 4.4 As a person giving out referrals, I need to be able to communicate requirements to get a referral from me so that I don’t get applicants who have no chance.
-- Add or update referral requirements in the Referrer table
UPDATE Referrer
SET contactInfo = 'Have 2+ years of experience'
WHERE referrerId = 100;

-- Story 4.5 As a person giving out referrals, I need to be able to see if any of my applicants have already gotten a referral from someone else to my company.
SELECT C.studentId, S.name AS studentName, R.company AS referredCompany, C.creationDate AS referralDate, Req.status AS applicationStatus
FROM Connections C
JOIN Referrer R ON C.referrerId = R.referrerId
JOIN Students S ON C.studentId = S.studentId
JOIN Requests Req ON Req.studentId = S.studentId AND Req.referrerId = R.referrerId

-- Story 4.6 As a person giving out referrals, I need to be able to add contact information, including people who can help contact or connect with me, so that people meeting me have a reference to help with interpersonal connection.
UPDATE Referrer
SET contactInfo = 'Email: @gmail.com'






