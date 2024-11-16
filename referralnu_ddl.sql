-- Create the database
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
    connectionId INT NOT NULL,
    PRIMARY KEY connectionId (referrerId, studentId),
    referrerId   INT NOT NULL,
    creationDate TIMESTAMP,
    studentId    INT NOT NULL,
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
    studentId   INT NOT NULL,
    referrerId  INT NOT NULL,
    status      VARCHAR(50),
    requestDate TIMESTAMP,
    industryId  INT NOT NULL,
    createdAt   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (studentId, referrerId),
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (industryId) REFERENCES Industries (industryId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create Messages table
CREATE TABLE Messages
(
    messageId      INT PRIMARY KEY NOT NULL,
    messageContent TEXT            NOT NULL,
    adminId        INT             NOT NULL,
    sentAt         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    connectionId   INT             NOT NULL,
    FOREIGN KEY (adminId) REFERENCES Admin (adminId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (connectionId) REFERENCES Connections (connectionId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);