USE referralnu;

-- User Persona 1: Admin

-- Story 1: As an administrator, I need to be able to verify that referral offers are from real employees so that the app doesn’t get fake referral offers.

SELECT ref.Name, ref.Company FROM Requests req
JOIN Referrer ref ON req.referrerId = ref.referrerId;

-- Story 2: As an administrator, I need to be able to cut connections that are not considered appropriate and productive to ensure students’ referral searches are as smooth as possible
-- First we want to find all the messages that contain bad words, then we want to delete the connections that are associated with those messages.
SELECT m.Message, m.studentId
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
SELECT c.status, m.Message
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

-- Story 4: As a referral seeker, I need to be able to view upcoming networking events hosted by my target companies so that I can connect with potential referrers directly.
-- NEED TO CREATE ANOTHER TABLE FOR COMPANY EVENTS???

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