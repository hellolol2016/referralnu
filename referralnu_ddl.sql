-- Create the database
CREATE DATABASE IF NOT EXISTS referralnu;
USE referralnu;

-- Create Advisor table
CREATE TABLE Advisor (
  advisorID INT PRIMARY KEY,
  name VARCHAR(255),
  contactInfo TEXT,
  college VARCHAR(255)
);

-- Create Students table
CREATE TABLE Students (
  studentId INT PRIMARY KEY,
  name VARCHAR(255),
  contactInfo TEXT,
  advisorId INT,
  FOREIGN KEY (advisorId) REFERENCES Advisor(advisorID)
);

-- Create Admin table
CREATE TABLE Admin (
  adminId INT PRIMARY KEY,
  name VARCHAR(255),
  contactInfo TEXT
);

-- Create Industries table
CREATE TABLE Industries (
  industryId INT PRIMARY KEY,
  name VARCHAR(255)
);

-- Create Referrer table
CREATE TABLE Referrer (
  referrerId INT PRIMARY KEY,
  name VARCHAR(255),
  contactInfo TEXT,
  creationDate TIMESTAMP,
  updateDate TIMESTAMP,
  company VARCHAR(255),
  adminId INT,
  industryId INT,
  FOREIGN KEY (adminId) REFERENCES Admin(adminId),
  FOREIGN KEY (industryId) REFERENCES Industries(industryId)
);

-- Create Connections table
CREATE TABLE Connections (
  connectionId INT PRIMARY KEY,
  referrerId INT,
  creationDate TIMESTAMP,
  studentId INT,
  FOREIGN KEY (referrerId) REFERENCES Referrer(referrerId),
  FOREIGN KEY (studentId) REFERENCES Students(studentId)
);

-- Create Requests table
CREATE TABLE Requests (
  studentId INT,
  referrerId INT,
  status VARCHAR(50),
  requestDate TIMESTAMP,
  industryId INT,
  PRIMARY KEY (studentId, referrerId),
  FOREIGN KEY (studentId) REFERENCES Students(studentId),
  FOREIGN KEY (referrerId) REFERENCES Referrer(referrerId),
  FOREIGN KEY (industryId) REFERENCES Industries(industryId)
);

-- Create Messages table
CREATE TABLE Messages (
  messageId INT PRIMARY KEY,
  messageContent TEXT,
  adminId INT,
  sentAt TIMESTAMP,
  connectionId INT,
  FOREIGN KEY (adminId) REFERENCES Admin(adminId),
  FOREIGN KEY (connectionId) REFERENCES Connections(connectionId)
);