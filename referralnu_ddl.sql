-- Create the database
DROP DATABASE IF EXISTS referralnu;
CREATE DATABASE IF NOT EXISTS referralnu;
USE referralnu;

-- Create Advisor table
CREATE TABLE Advisor
(
    advisorID   INT PRIMARY KEY AUTO_INCREMENT,
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
    FOREIGN KEY (advisorId) REFERENCES Advisor (advisorID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Create Admin table
CREATE TABLE Admin
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

-- Create Referrer table
CREATE TABLE Referrer
(
    referrerId   INT PRIMARY KEY AUTO_INCREMENT,
    name         VARCHAR(255) NOT NULL,
    email        VARCHAR(255) NOT NULL,
    phoneNumber  VARCHAR(20),
    creationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updateDate   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    company      VARCHAR(255) NOT NULL,
    adminId      INT          NOT NULL,
    industryId   INT          NOT NULL,
    numReferrals INT,
    FOREIGN KEY (adminId) REFERENCES Admin (adminId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (industryId) REFERENCES Industries (industryId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Create Connections table
CREATE TABLE Connections
(
    CONSTRAINT connectionId PRIMARY KEY (referrerId, studentId),
    referrerId   INT NOT NULL,
    creationDate TIMESTAMP,
    studentId    INT NOT NULL,
    companyName VARCHAR(255) NOT NULL,
    FOREIGN KEY (referrerId) REFERENCES Referrer (referrerId)
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
    industryId  INT NOT NULL,
    createdAt   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastViewed  TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    viewCount   INT,
    companyName VARCHAR(255) NOT NULL,
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (industryId) REFERENCES Industries (industryId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Advice
{
    studentId INT,
    advisorId INT,
    sendDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    readDate TIMESTAMP
    readStatus VARCHAR(50),
    content TEXT,
    followUpDate TIMESTAMP
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (advisorId) REFERENCES Advisor (advisorId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
};

-- Create Messages table
CREATE TABLE Messages
(
    messageId      INT PRIMARY KEY NOT NULL,
    messageContent TEXT            NOT NULL,
    adminId        INT             NOT NULL,
    sentAt         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    connectionId   INT             NOT NULL,
    referrerId     INT             NOT NULL,
    studentId      INT             NOT NULL,
    FOREIGN KEY (adminId) REFERENCES Admin (adminId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (referrerId, studentId) REFERENCES Connections (referrerId, studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

INSERT INTO Advisor (firstName, lastName, email, phoneNumber, college)
VALUES
('John', 'Doe', 'johndoe@example.com', '555-1234', 'Harvard University'),
('Jane', 'Smith', 'janesmith@example.com', '555-5678', 'MIT'),
('Emily', 'Johnson', 'emilyjohnson@example.com', '555-8765', 'Boston University');

INSERT INTO Students (firstName, lastName, email, phoneNumber, advisorId)
VALUES
('Alice', 'Green', 'alicegreen@example.com', '555-1122', 1),
('Bob', 'Brown', 'bobbrown@example.com', '555-2233', 2),
('Charlie', 'White', 'charliewhite@example.com', '555-3344', 3);

INSERT INTO Admin (firstName, lastName, email, phoneNumber)
VALUES
('Sarah', 'Lee', 'sarahlee@example.com', '555-4455'),
('Tom', 'Walker', 'tomwalker@example.com', '555-5566');

INSERT INTO Industries (industryId, name)
VALUES
(1, 'Technology'),
(2, 'Healthcare'),
(3, 'Finance');

INSERT INTO Referrer (name, email, phoneNumber, company, adminId, industryId, numReferrals)
VALUES
('David Wilson', 'davidwilson@techcorp.com', '555-6677', 'TechCorp', 1, 1, 5),
('Rachel Adams', 'racheladams@healthcareinc.com', '555-7788', 'HealthcareInc', 2, 2, 3);

INSERT INTO Connections (referrerId, studentId, companyName)
VALUES
(1, 1, 'Google'),
(2, 2, 'Amazon'),
(1, 3, 'FaceBook');

INSERT INTO Requests (studentId, pendingStatus, industryId, companyName)
VALUES
(1, 'Pending', 1, 'Google'),
(2,  'Accepted', 2, 'Amazon'),
(3,  'Rejected', 3, 'FaceBook');

INSERT INTO Messages (messageId, messageContent, adminId, connectionId, referrerId, studentId)
VALUES
(1, 'Welcome to the program!', 1, 1, 1, 1),
(2, 'Your request has been accepted.', 2, 2, 2, 2),
(3, 'Unfortunately, your request has been rejected.', 1, 3, 1, 3);
