-- Create the database
DROP DATABASE IF EXISTS referralnu;
CREATE DATABASE IF NOT EXISTS referralnu;
USE referralnu;

-- Create Advisor table
CREATE TABLE Advisors
(
    advisorId   INT PRIMARY KEY AUTO_INCREMENT,
    firstName   VARCHAR(20)  NOT NULL,
    lastName    VARCHAR(40)  NOT NULL,
    email       VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(20),
    college     VARCHAR(255) NOT NULL
);

-- Create Students table
CREATE TABLE Students
(
    studentId   INT PRIMARY KEY AUTO_INCREMENT,
    firstName   VARCHAR(20)  NOT NULL,
    lastName    VARCHAR(40)  NOT NULL,
    email       VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(20),
    advisorId   INT,
    FOREIGN KEY (advisorId) REFERENCES Advisors (advisorID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Create Admin table
CREATE TABLE Admins
(
    adminId     INT PRIMARY KEY AUTO_INCREMENT,
    firstName   VARCHAR(20)  NOT NULL,
    lastName    VARCHAR(40)  NOT NULL,
    email       VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(20)
);

-- Create Industries table
CREATE TABLE Industries
(
    industryId INT PRIMARY KEY NOT NULL,
    name       VARCHAR(255)    NOT NULL
);

CREATE TABLE Companies
(
    companyId  INT PRIMARY KEY AUTO_INCREMENT,
    name       VARCHAR(255) NOT NULL,
    industryId INT          NOT NULL,
    FOREIGN KEY (industryId) REFERENCES Industries (industryId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create Referrer table
CREATE TABLE Referrers
(
    referrerId   INT PRIMARY KEY AUTO_INCREMENT,
    name         VARCHAR(255) NOT NULL,
    email        VARCHAR(255) NOT NULL,
    phoneNumber  VARCHAR(20),
    creationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updateDate   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    adminId      INT          NOT NULL,
    companyId   INT          NOT NULL,
    numReferrals INT,
    FOREIGN KEY (adminId) REFERENCES Admins (adminId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (companyId) REFERENCES Companies (companyId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Create Connections table
CREATE TABLE Connections
(
    connectionId INT PRIMARY KEY AUTO_INCREMENT,
    referrerId   INT NOT NULL,
    creationDate TIMESTAMP,
    studentId    INT NOT NULL,
    FOREIGN KEY (referrerId) REFERENCES Referrers (referrerId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);



-- Create Requests table
CREATE TABLE Requests
(
    requestId   INT PRIMARY KEY AUTO_INCREMENT,
    studentId   INT NOT NULL,
    pendingStatus      VARCHAR(50),
    requestDate TIMESTAMP,
    companyId  INT NOT NULL,
    createdAt   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastViewed  TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    viewCount   INT,
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (companyId) REFERENCES Companies (companyId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Advisor_Messages
(
    studentId      INT Not NULL,
    advisorId      INT Not NULL,
    sendDate       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    readDate       TIMESTAMP DEFAULT NULL,
    readStatus     ENUM('read', 'unread') DEFAULT 'unread',
    content        TEXT NOT NULL,
    followUpDate   TIMESTAMP DEFAULT (DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 DAY)),
    reminderStatus ENUM('pending', 'sent', 'none') DEFAULT 'none',
    messageId      INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (advisorId) REFERENCES Advisors (advisorId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);



-- Create Messages table
CREATE TABLE Messages
(
    messageId      INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    messageContent TEXT            NOT NULL,
    adminId        INT             NOT NULL,
    sentAt         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    connectionId   INT             NOT NULL,
    referrerId     INT             NOT NULL,
    studentId      INT             NOT NULL,
    studentSent    BOOLEAN         NOT NULL,
    FOREIGN KEY (adminId) REFERENCES Admins (adminId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (connectionId) REFERENCES Connections (connectionId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX idx_advisorId ON Students (advisorId);

INSERT INTO Advisors (firstName, lastName, email, phoneNumber, college)
VALUES
('John', 'Doe', 'johndoe@example.com', '555-1234', 'Harvard University'),
('Jane', 'Smith', 'janesmith@example.com', '555-5678', 'MIT'),
('Emily', 'Johnson', 'emilyjohnson@example.com', '555-8765', 'Boston University');

INSERT INTO Students (firstName, lastName, email, phoneNumber, advisorId)
VALUES
('Alice', 'Green', 'alicegreen@example.com', '555-1122', 1),
('Bob', 'Brown', 'bobbrown@example.com', '555-2233', 2),
('Charlie', 'White', 'charliewhite@example.com', '555-3344', 3);

INSERT INTO Admins (firstName, lastName, email, phoneNumber)
VALUES
('Sarah', 'Lee', 'sarahlee@example.com', '555-4455'),
('Tom', 'Walker', 'tomwalker@example.com', '555-5566');

INSERT INTO Industries (industryId, name)
VALUES
(1, 'Technology'),
(2, 'Healthcare'),
(3, 'Finance');

INSERT INTO Companies (name, industryId)
VALUES
('Tech Innovators Inc.', 1),
('HealthFirst Solutions', 2),
('Future Finance Co.', 3);

INSERT INTO Referrers (name, email, phoneNumber, adminId, companyId, numReferrals)
VALUES
('David Wilson', 'davidwilson@techcorp.com', '555-6677',  1, 1, 5),
('Rachel Adams', 'racheladams@healthcareinc.com', '555-7788',  2, 2, 3);

INSERT INTO Connections (referrerId, studentId)
VALUES
(1, 1),
(2, 2),
(1, 3);

INSERT INTO Requests (studentId, pendingStatus, companyId)
VALUES
(1, 'Pending', 1),
(2,  'Accepted', 2),
(3,  'Rejected', 3);

INSERT INTO Messages (messageContent, adminId, connectionId, referrerId, studentId,studentSent)
VALUES
('Welcome to the program!', 1, 1, 1, 1, false),
('Your request has been accepted.', 2, 2, 2, 2, false),
('Unfortunately, your request has been rejected.', 1, 3, 1, 3,false),
('GOSH DANG IT!', 1, 3, 1, 3,true);

INSERT INTO Advisor_Messages (studentId, advisorId, sendDate, readDate, readStatus, content, followUpDate)
VALUES
(1, 1, '2024-11-16 10:00:00', NULL, 'unread', 'Meeting scheduled for next week.', '2024-11-19 10:00:00'),
(2, 2, '2024-11-15 15:30:00', '2024-11-16 09:00:00', 'read', 'Please review the course materials.', '2024-11-18 15:30:00'),
(3, 3, DEFAULT, NULL, 'unread', 'Your application has been submitted.', DEFAULT);
