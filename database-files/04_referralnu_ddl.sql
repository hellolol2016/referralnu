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
    industryId INT PRIMARY KEY AUTO_INCREMENT,
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
    creationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    studentId    INT NOT NULL,
    FOREIGN KEY (referrerId) REFERENCES Referrers (referrerId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (studentId) REFERENCES Students (studentId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);



-- Create Requests table
CREATE TABLE Requests
(
    requestId   INT PRIMARY KEY AUTO_INCREMENT,
    studentId   INT NOT NULL,
    pendingStatus      VARCHAR(50),
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

INSERT INTO Advisors (firstName, lastName, email, phoneNumber, college) VALUES
('Chrysa', 'Chillistone', 'cchillistone0@meetup.com', '657-558-3595', 'Bouve College of Health Sciences'),
('Filip', 'Truran', 'ftruran1@people.com.cn', '765-823-5582', 'Khoury College of Computer Science'),
('Gary', 'Seath', 'gseath2@nba.com', '736-514-5575', 'Northeastern University School of Law'),
('Chrystel', 'Nicholl', 'cnicholl3@usnews.com', '875-408-7236', 'Mills College'),
('Nicola', 'Elphinstone', 'nelphinstone4@goodreads.com', '292-904-4853', 'D''Amore-McKim School of Business'),
('Agace', 'Godridge', 'agodridge5@spiegel.de', '681-146-8779', 'Bouve College of Health Sciences'),
('Lazar', 'Weston', 'lweston6@yahoo.co.jp', '340-858-2778', 'College of Humanities and Social Science'),
('Vidovic', 'Meadley', 'vmeadley7@nymag.com', '878-246-7691', 'College of Arts Media and Design'),
('Harmonia', 'Thompsett', 'hthompsett8@wisc.edu', '937-790-1617', 'D''Amore-McKim School of Business'),
('Yorke', 'McGrail', 'ymcgrail9@bluehost.com', '544-237-6068', 'College of Professional Studies'),
('Carlie', 'Gauche', 'cgauchea@livejournal.com', '467-949-1301', 'Bouve College of Health Sciences'),
('Gram', 'Swatton', 'gswattonb@cpanel.net', '827-712-2364', 'College of Humanities and Social Science'),
('Enrika', 'Nelm', 'enelmc@wikimedia.org', '411-840-3425', 'Northeastern University School of Law'),
('Alis', 'Kowalski', 'akowalskid@paginegialle.it', '213-707-2190', 'Mills College'),
('Jo-anne', 'Shaddock', 'jshaddocke@digg.com', '281-175-0842', 'Khoury College of Computer Science'),
('Nichols', 'Jorg', 'njorgf@dell.com', '900-723-2296', 'Khoury College of Computer Science'),
('Tabitha', 'Tompkins', 'ttompkinsg@nationalgeographic.com', '716-401-5762', 'D''Amore-McKim School of Business'),
('Sella', 'Chene', 'scheneh@51.la', '797-948-7035', 'College of Science'),
('Loella', 'Jakoubek', 'ljakoubeki@123-reg.co.uk', '609-138-4240', 'College of Engineering'),
('Callida', 'Van De Cappelle', 'cvandecappellej@nationalgeographic.com', '779-459-8648', 'Northeastern University School of Law'),
('Shir', 'Dusting', 'sdustingk@ucla.edu', '925-517-9915', 'College of Professional Studies'),
('Carolina', 'Cubley', 'ccubleyl@merriam-webster.com', '213-997-6170', 'Northeastern University School of Law'),
('Bibi', 'Oliffe', 'boliffem@gnu.org', '748-179-7131', 'College of Professional Studies'),
('Chrissy', 'Blowers', 'cblowersn@berkeley.edu', '989-360-6901', 'Northeastern University School of Law'),
('Cam', 'Canto', 'ccantoo@wikia.com', '194-899-1339', 'College of Engineering'),
('Reine', 'Varden', 'rvardenp@nasa.gov', '394-230-5804', 'College of Professional Studies'),
('Cleve', 'Piggen', 'cpiggenq@illinois.edu', '621-339-6237', 'College of Engineering'),
('Dido', 'Itzkovsky', 'ditzkovskyr@disqus.com', '142-734-9140', 'D''Amore-McKim School of Business'),
('Heddi', 'Velti', 'hveltis@cdbaby.com', '184-288-0109', 'College of Science'),
('Gillan', 'Lebreton', 'glebretont@mit.edu', '115-291-9845', 'Khoury College of Computer Science'),
('Filia', 'Johann', 'fjohannu@rambler.ru', '298-626-7511', 'Northeastern University School of Law'),
('Nata', 'Rilston', 'nrilstonv@drupal.org', '631-971-5691', 'Bouve College of Health Sciences'),
('Kristoffer', 'McEnery', 'kmceneryw@trellian.com', '333-789-9096', 'College of Engineering'),
('Lari', 'Moyes', 'lmoyesx@fema.gov', '279-648-1043', 'College of Professional Studies'),
('Beauregard', 'Bulluck', 'bbullucky@gizmodo.com', '986-787-0275', 'College of Humanities and Social Science'),
('Heinrick', 'Spenceley', 'hspenceleyz@cnbc.com', '298-418-0400', 'College of Arts Media and Design'),
('Alonso', 'Pick', 'apick10@gnu.org', '836-954-1290', 'Northeastern University School of Law'),
('Kerianne', 'Grafton', 'kgrafton11@clickbank.net', '874-632-4887', 'D''Amore-McKim School of Business'),
('Kerrin', 'Lafontaine', 'klafontaine12@eepurl.com', '807-965-7507', 'College of Science'),
('Kaleb', 'MacCallion', 'kmaccallion13@yelp.com', '806-111-0375', 'Northeastern University School of Law');


insert into Students (firstName, lastName, email, phoneNumber, advisorId) 
values 
('Seamus', 'Goodby', 'sgoodby0@walmart.com', '338-712-5541', 37),
('Garland', 'Manton', 'gmanton1@dyndns.org', '725-996-0535', 34),
('Codee', 'Ashcroft', 'cashcroft2@jalbum.net', '700-438-5984', 6),
('Darb', 'Williams', 'dwilliams3@yelp.com', '702-803-4055', 22),
('Kennith', 'Defont', 'kdefont4@webs.com', '438-839-1824', 39),
('Austin', 'Dyers', 'adyers5@360.cn', '746-948-9671', 11),
('Veriee', 'Aslam', 'vaslam6@webnode.com', '773-855-1092', 40),
('Nata', 'Friedlos', 'nfriedlos7@tuttocitta.it', '801-465-9814', 14),
('Krystal', 'Kirkam', 'kkirkam8@goo.ne.jp', '811-417-0590', 36),
('Nealon', 'Pretty', 'npretty9@flickr.com', '965-174-7258', 18),
('Ulberto', 'Willshaw', 'uwillshawa@apple.com', '245-472-8880', 31),
('Page', 'Luto', 'plutob@dell.com', '419-320-0874', 17),
('Esme', 'Maker', 'emakerc@google.nl', '823-860-6143', 3),
('Bellanca', 'Chesshire', 'bchesshired@webnode.com', '675-688-3541', 36),
('Sandra', 'Merrison', 'smerrisone@archive.org', '658-314-8022', 20),
('Den', 'Ferraretto', 'dferrarettof@illinois.edu', '393-518-5196', 4),
('Nonnah', 'Shearman', 'nshearmang@tinyurl.com', '183-121-2210', 11),
('Clemente', 'Cordet', 'ccordeth@gizmodo.com', '528-589-3120', 11),
('Nonna', 'Ainsley', 'nainsleyi@fema.gov', '777-267-0736', 24),
('Alane', 'Winstone', 'awinstonej@mozilla.org', '386-617-4568', 3),
('Aleda', 'Saintsbury', 'asaintsburyk@princeton.edu', '563-724-2917', 9),
('Bail', 'Coverdill', 'bcoverdilll@freewebs.com', '764-557-0777', 9),
('Livy', 'Vickers', 'lvickersm@businessinsider.com', '496-323-6910', 13),
('Brinna', 'Gellately', 'bgellatelyn@rediff.com', '244-593-7041', 6),
('Gail', 'Angelo', 'gangeloo@about.me', '882-517-6633', 22),
('Jemima', 'Simpkiss', 'jsimpkissp@spiegel.de', '552-558-7493', 32),
('Charita', 'Pellant', 'cpellantq@ow.ly', '126-998-5287', 27),
('Duke', 'Scheu', 'dscheur@cdbaby.com', '235-114-2374', 3),
('Margalit', 'Merveille', 'mmerveilles@mediafire.com', '187-829-6102', 32),
('Chiquia', 'Wynter', 'cwyntert@bluehost.com', '720-920-3991', 6),
('Orazio', 'Pelz', 'opelzu@whitehouse.gov', '790-285-6029', 36),
('Aloysia', 'Keddey', 'akeddeyv@si.edu', '815-742-1936', 5),
('Karlan', 'Sturmey', 'ksturmeyw@ehow.com', '296-754-7717', 12),
('Daffi', 'Pomeroy', 'dpomeroyx@wordpress.com', '120-564-2908', 18),
('Tessy', 'Pentercost', 'tpentercosty@soup.io', '186-174-2843', 38),
('Tedmund', 'Clementel', 'tclementelz@ibm.com', '221-904-6792', 8),
('Gabie', 'Baldini', 'gbaldini10@fema.gov', '850-879-4474', 20),
('Frederik', 'McReedy', 'fmcreedy11@newyorker.com', '400-420-4840', 3),
('Ganny', 'Hansard', 'ghansard12@ebay.co.uk', '213-193-3460', 38),
('Andonis', 'Joskovitch', 'ajoskovitch13@webnode.com', '709-972-3227', 29);


INSERT INTO Admins (firstName, lastName, email, phoneNumber) VALUES
("Eddy", "Gryglewski", "egryglewski0@google.ca", "660-887-6739"),
("Taber", "Rispen", "trispen1@skype.com", "136-288-0413"),
("Ami", "Surr", "asurr2@deliciousdays.com", "517-235-7495"),
("Didi", "Eason", "deason3@webnode.com", "568-584-5921"),
("Sylas", "Lauridsen", "slauridsen4@wikia.com", "919-476-0438"),
("Emilee", "Branwhite", "ebranwhite5@unc.edu", "325-513-8613"),
("Almire", "Meeke", "ameeke6@constantcontact.com", "995-217-4944"),
("Marietta", "Athersmith", "mathersmith7@netvibes.com", "830-231-2830"),
("Ariana", "Van Dijk", "avandijk8@hc360.com", "934-215-3269"),
("Patrica", "Niesel", "pniesel9@tripadvisor.com", "499-131-4957"),
("Jamal", "Lording", "jlordinga@tripod.com", "350-548-9200"),
("Domini", "Busek", "dbusekb@mozilla.org", "578-833-0254"),
("Algernon", "Gatrill", "agatrillc@illinois.edu", "365-444-2208"),
("Rinaldo", "Fasse", "rfassed@scribd.com", "776-427-2553"),
("Ganny", "Doumer", "gdoumere@reference.com", "174-738-1646"),
("Georgia", "Howcroft", "ghowcroftf@tmall.com", "311-913-0980"),
("Conan", "Willimott", "cwillimottg@livejournal.com", "757-350-3286"),
("Bryanty", "Kwiek", "bkwiekh@so-net.ne.jp", "890-725-2576"),
("Russell", "Wonfor", "rwonfori@surveymonkey.com", "309-924-5725"),
("Aldrich", "Glasspoole", "aglasspoolej@oaic.gov.au", "188-133-9555"),
("Chaddie", "O'Doherty", "codohertyk@theglobeandmail.com", "291-431-4691"),
("Yuri", "Taaffe", "ytaaffel@nydailynews.com", "251-971-1219"),
("Filmore", "Ferrero", "fferrerom@feedburner.com", "390-367-2860"),
("Alethea", "Brighty", "abrightyn@discovery.com", "867-682-9582"),
("Arthur", "Govini", "agovinio@bbc.co.uk", "382-200-8994"),
("Wally", "Simyson", "wsimysonp@gmpg.org", "595-930-5065"),
("Sophia", "Gowans", "sgowansq@harvard.edu", "627-636-8722"),
("Sigismund", "Jolley", "sjolleyr@mayoclinic.com", "164-212-2883"),
("Yolande", "Dullingham", "ydullinghams@jimdo.com", "943-566-5590"),
("Nobe", "Mathis", "nmathist@patch.com", "620-668-8953"),
("Yovonnda", "Ouldcott", "youldcottu@unc.edu", "673-224-8141"),
("Xerxes", "Smiley", "xsmileyv@naver.com", "797-318-1916"),
("Nero", "Gouldstraw", "ngouldstraww@msu.edu", "855-571-8574"),
("Hinze", "Agglione", "hagglionex@marriott.com", "243-348-2939"),
("Claribel", "Coper", "ccopery@mlb.com", "200-442-2855"),
("Elene", "Strickland", "estricklandz@youku.com", "208-689-4337"),
("Layne", "Odom", "lodom10@walmart.com", "853-215-7239"),
("Zechariah", "Palluschek", "zpalluschek11@ebay.co.uk", "691-939-0258"),
("Patsy", "Fleckney", "pfleckney12@nih.gov", "955-532-7145"),
("Royal", "Millott", "rmillott13@vinaora.com", "236-127-7447");


INSERT INTO Industries (name) VALUES
("Industrial Machinery/Components"),
("Major Chemicals"),
("Major Banks"),
("Major Pharmaceuticals"),
("Telecommunications Equipment"),
("EDP Services"),
("Electronic Components"),
("Marine Transportation"),
("Business Services"),
("Real Estate Investment Trusts"),
("Property-Casualty Insurers"),
("Coal Mining"),
("Computer Communications Equipment"),
("Broadcasting"),
("Biotechnology: In Vitro & In Vivo Diagnostic Substances"),
("Medical/Dental Instruments"),
("Computer Software: Prepackaged Software"),
("Services-Misc. Amusement & Recreation"),
("Beverages (Production/Distribution)");


INSERT INTO Companies (name, industryId) VALUES
("Streich-Greenfelder", 1),
("Rohan and Sons", 2),
("Koss, Cartwright and Walter", 11),
("Denesik, Leffler and Gleichner", 17),
("Mitchell-Graham", 13),
("Hamill, Cartwright and Littel", 5),
("Schultz and Sons", 16),
("Russel LLC", 5),
("Nicolas, Mertz and Ankunding", 13),
("Oberbrunner and Sons", 18),
("Lehner LLC", 5),
("Lockman Inc", 18),
("Fahey, Wolf and Macejkovic", 4),
("Dicki, Anderson and Bednar", 11),
("Douglas Inc", 9),
("Hane-Kautzer", 12),
("Fadel and Sons", 7),
("Collier, Rodriguez and Abshire", 15),
("Frami-McKenzie", 3),
("McDermott Inc", 13),
("Johnson-Harber", 17),
("Johnson Inc", 16),
("Ullrich, Littel and Koelpin", 9),
("Herman, Shanahan and Hettinger", 17),
("Nienow, Jaskolski and Wisozk", 11),
("Kutch-Pollich", 17),
("Kuhlman-Larkin", 7),
("Weissnat Inc", 2),
("Swift, Fahey and Cormier", 14),
("Gottlieb-Roberts", 12),
("Heller Inc", 4),
("Klein-Roberts", 18),
("Metz-Haag", 14),
("Hagenes Group", 2),
("Hammes, Schmeler and Ward", 6),
("Hammes, Grimes and Lakin", 11),
("Leannon and Sons", 14),
("Vandervort Group", 15),
("Huels Group", 18),
("Kessler-Durgan", 9);


INSERT INTO Referrers (name, email, phoneNumber, adminId, companyId, numReferrals) VALUES
("Gwenneth Vallens", "gvallens0@cam.ac.uk", "226-755-0645", 8, 20, 4),
("Ferris Boshell", "fboshell1@networksolutions.com", "313-292-8059", 32, 17, 5),
("Savina Kirkwood", "skirkwood2@cmu.edu", "540-821-3827", 25, 3, 2),
("Moshe Bourdon", "mbourdon3@redcross.org", "249-754-3211", 9, 32, 5),
("Mauricio Fosdyke", "mfosdyke4@youtu.be", "771-856-1511", 15, 40, 3),
("Ketty Haggerwood", "khaggerwood5@ebay.co.uk", "981-254-9256", 23, 6, 5),
("Gordy Hardbattle", "ghardbattle6@pbs.org", "549-783-9831", 29, 11, 3),
("Des Pisculli", "dpisculli7@google.ca", "974-444-0436", 4, 20, 3),
("Shoshana Menpes", "smenpes8@uol.com.br", "302-576-6187", 6, 13, 1),
("Emily Loosely", "eloosely9@dedecms.com", "492-239-4842", 13, 19, 5),
("Aleta Daldan", "adaldana@studiopress.com", "897-513-9935", 10, 6, 4),
("Russell Tolliday", "rtollidayb@twitpic.com", "791-144-8727", 38, 8, 4),
("Burton Verring", "bverringc@amazon.com", "779-181-2650", 4, 6, 5),
("Torry Noni", "tnonid@indiegogo.com", "500-715-5084", 11, 36, 2),
("Teena Delicate", "tdelicatee@addtoany.com", "577-601-0796", 32, 30, 3),
("Kassandra Jannaway", "kjannawayf@weebly.com", "310-195-5077", 28, 16, 2),
("Lemar Sperry", "lsperryg@4shared.com", "452-415-5179", 34, 3, 2),
("Chancey Minett", "cminetth@mtv.com", "828-901-7849", 38, 12, 3),
("Bernete Koba", "bkobai@mayoclinic.com", "672-276-6867", 4, 12, 5),
("Benedetto Henriet", "bhenrietj@hud.gov", "203-853-5914", 29, 23, 4),
("Raymund Talbot", "rtalbotk@blogs.com", "204-305-1354", 27, 10, 3),
("Carroll Heinssen", "cheinssenl@exblog.jp", "408-967-3672", 27, 22, 2),
("Kiersten Yankov", "kyankovm@yahoo.com", "240-974-6765", 10, 1, 2),
("Ethan Weddup", "eweddupn@ucoz.com", "607-475-3740", 7, 33, 2),
("Dotty Guilder", "dguildero@thetimes.co.uk", "458-618-4865", 29, 21, 1),
("Kit McKibbin", "kmckibbinp@g.co", "767-804-9492", 38, 2, 5),
("Orlando De Minico", "odeq@google.com.br", "730-728-9232", 1, 16, 1),
("Jen Rosita", "jrositar@who.int", "547-617-0232", 30, 8, 2),
("George Bustin", "gbustins@studiopress.com", "599-484-3565", 11, 13, 2),
("Stevie Ifill", "sifillt@cnbc.com", "973-772-0983", 19, 21, 5),
("Sheridan Surcombe", "ssurcombeu@google.com.br", "347-626-9341", 1, 2, 5),
("Randolph Langlands", "rlanglandsv@miitbeian.gov.cn", "420-199-5185", 16, 26, 2),
("Clotilda Torra", "ctorraw@comcast.net", "949-676-6488", 38, 35, 2),
("Al Quirk", "aquirkx@arizona.edu", "614-109-5665", 28, 40, 1),
("Northrup Vicent", "nvicenty@posterous.com", "923-718-1803", 27, 36, 5),
("Pru MacIver", "pmaciverz@taobao.com", "446-122-1422", 20, 39, 1),
("Balduin Nester", "bnester10@istockphoto.com", "856-662-5777", 39, 29, 5),
("Vergil Farady", "vfarady11@woothemes.com", "209-661-9111", 31, 14, 3),
("Beaufort Barnaclough", "bbarnaclough12@bravesites.com", "971-773-2454", 8, 10, 3),
("Alvis Campo", "acampo13@alibaba.com", "643-740-2338", 16, 21, 5);


INSERT INTO Connections (referrerId, studentId) 
VALUES 
(19, 6), 
(24, 39), 
(40, 8), 
(12, 3), 
(24, 24), 
(21, 23), 
(4, 19), 
(12, 28), 
(13, 32), 
(13, 33), 
(33, 4), 
(7, 6), 
(38, 22), 
(37, 11), 
(22, 27), 
(33, 31), 
(29, 4), 
(35, 20), 
(19, 27), 
(31, 23), 
(3, 14), 
(40, 29), 
(13, 18), 
(25, 24), 
(30, 1), 
(27, 7), 
(15, 14), 
(39, 18), 
(35, 25), 
(24, 38), 
(39, 16), 
(25, 8), 
(31, 14), 
(36, 25), 
(20, 19), 
(3, 14), 
(33, 9), 
(25, 33), 
(23, 13), 
(7, 32), 
(21, 35), 
(3, 29), 
(40, 11), 
(22, 25), 
(18, 33), 
(3, 37), 
(29, 34), 
(33, 19), 
(5, 37), 
(15, 16), 
(17, 17), 
(8, 6), 
(3, 8), 
(14, 38), 
(11, 30), 
(12, 26), 
(33, 16), 
(8, 26), 
(32, 36), 
(21, 38), 
(33, 5), 
(10, 23), 
(32, 1), 
(11, 27), 
(5, 15), 
(34, 7), 
(15, 36), 
(19, 9), 
(5, 3), 
(4, 36), 
(33, 22), 
(32, 13), 
(14, 33), 
(5, 39), 
(8, 16), 
(27, 24), 
(22, 11), 
(28, 37), 
(24, 27), 
(1, 22);


INSERT INTO Requests (studentId, pendingStatus, companyId) 
VALUES 
(15, 'pending', 35),
(8, 'rejected', 18),
(39, 'pending', 10),
(34, 'accepted', 7),
(39, 'rejected', 4),
(38, 'accepted', 21),
(9, 'rejected', 30),
(3, 'accepted', 28),
(29, 'rejected', 19),
(7, 'pending', 5),
(26, 'accepted', 2),
(20, 'rejected', 11),
(39, 'rejected', 24),
(19, 'pending', 18),
(36, 'pending', 23),
(8, 'pending', 39),
(35, 'accepted', 29),
(15, 'pending', 27),
(33, 'pending', 7),
(17, 'rejected', 16),
(4, 'pending', 9),
(15, 'pending', 40),
(9, 'accepted', 19),
(30, 'accepted', 28),
(27, 'accepted', 15),
(3, 'pending', 28),
(25, 'accepted', 18),
(4, 'pending', 23),
(2, 'pending', 19),
(37, 'accepted', 8),
(15, 'rejected', 37),
(3, 'pending', 25),
(16, 'rejected', 19),
(21, 'rejected', 29),
(19, 'accepted', 30),
(22, 'pending', 10),
(38, 'rejected', 3),
(31, 'pending', 5),
(26, 'rejected', 9),
(40, 'accepted', 22),
(9, 'accepted', 6),
(40, 'accepted', 11),
(9, 'accepted', 31),
(31, 'rejected', 14),
(23, 'accepted', 7),
(21, 'accepted', 23),
(11, 'rejected', 27),
(18, 'accepted', 24),
(26, 'pending', 3),
(37, 'accepted', 12),
(31, 'accepted', 4),
(27, 'pending', 13),
(24, 'rejected', 39),
(4, 'pending', 4),
(25, 'pending', 32),
(29, 'rejected', 6),
(8, 'rejected', 4),
(3, 'pending', 35),
(32, 'pending', 15),
(36, 'rejected', 7),
(24, 'accepted', 16),
(12, 'accepted', 22),
(35, 'rejected', 36),
(9, 'pending', 34),
(11, 'accepted', 2),
(6, 'accepted', 22),
(32, 'pending', 10),
(6, 'rejected', 5),
(32, 'rejected', 12),
(38, 'pending', 3),
(9, 'pending', 8),
(30, 'pending', 29),
(16, 'accepted', 7),
(30, 'accepted', 39),
(22, 'rejected', 12),
(19, 'pending', 40),
(6, 'accepted', 14),
(13, 'rejected', 31),
(9, 'accepted', 9),
(5, 'accepted', 37);


insert into Messages (messageContent, adminId, connectionId, referrerId, studentId, studentSent) values
('I hope you are doing well. I wanted to reach out to introduce myself and express my interest in learning more about your work in the industry.', 33, 24, 36, 20, true),
('I recently came across your work, and I am very interested in the insights you have shared on [specific topic]. I would love to hear more about your experience in the field.', 33, 57, 27, 11, true),
('Thank you for taking the time to meet with me. I found our conversation very valuable and would appreciate any advice you might have for someone entering the industry.', 21, 9, 28, 10, false),
('I hope this message finds you well. I am currently exploring career opportunities in [industry], and I would love to connect with you to learn more about your journey.', 32, 15, 40, 38, true),
('I have been following your career and am very impressed by your work. Would you be open to a brief conversation about your experience and any advice you have for someone starting out?', 21, 46, 22, 17, true),
('I will be attending [event/conference] next week, and I would love the opportunity to connect with you if you`re available during the event.', 31, 11, 11, 13, true),
('I`m currently exploring new opportunities in [industry] and would appreciate any guidance or referrals you may have regarding openings in the field.', 17, 80, 40, 25, false),
('I noticed you`re involved in [company/field], and I would love to learn more about your work. Would you be open to a coffee chat to discuss your experiences?', 25, 14, 14, 6, true),
('I`m currently navigating the job market and was wondering if you might have any recommendations or could share any referrals for opportunities in [specific area].', 38, 67, 29, 6, false),
('I wanted to check in and see if there might be any current opportunities at your company. I am very interested in the work you`re doing and would love to contribute.', 11, 70, 29, 10, true),
('I submitted my application for the [position] at [company]. If you have a moment, I`d really appreciate any insight or advice you can offer about the next steps in the hiring process.', 20, 33, 20, 36, false),
('I would like to schedule a time to talk about potential career opportunities and gain advice about the industry. Do you have any availability this week?', 35, 77, 18, 20, true),
('Could you provide more information on how you got started in [industry/field]? I`m seeking advice on how to build a career in this area.', 8, 31, 17, 8, true),
('Please let me know if there are any opportunities for internships or job openings at your organization that might be a good fit for someone with my background.', 24, 20, 39, 36, false),
('I have completed a few projects that are aligned with your work in [area]. Would you be willing to review my portfolio and provide any feedback or recommendations?', 18, 14, 22, 40, true),
('Could you provide feedback on my resume and cover letter? I`m looking to apply for [specific position] and would greatly appreciate your perspective.', 9, 68, 19, 8, false),
('I will be traveling next week and would love to connect before I leave to discuss opportunities and how I can best position myself for success in [field].', 11, 14, 37, 37, true),
('I reviewed your company`s recent achievements and am impressed. I would love the opportunity to speak with you about potential opportunities or advice you may have for someone entering the industry.', 32, 57, 17, 35, true),
('I`ve been learning about your work in [specific area], and I`d love the chance to chat and hear more about your career path and any tips for those entering the field.', 14, 41, 1, 13, true),
('Could you provide more information on how you navigated your career path in [industry]? I am hoping to make similar strides in my own career.', 15, 31, 4, 13, false),
('I`ve been keeping up with your updates on [platform] and would love the opportunity to connect and learn more about the work you`re doing.', 38, 24, 25, 29, false),
('I have some questions about your career journey and would greatly appreciate your insights. Would you be open to a quick meeting or call?', 33, 40, 25, 33, false),
('I`m interested in exploring opportunities in [industry]. Can you suggest any resources or organizations to explore?', 5, 14, 22, 8, false),
('I`d love to chat about your experience in [field]. Would you be available for a brief meeting or call to discuss potential paths in this area?', 20, 19, 2, 10, true),
('I`m considering taking a leave next semester to explore internships and would love to hear your thoughts on how to approach it while maintaining my academic progress.', 13, 71, 31, 29, true),
('I wanted to follow up on a previous conversation about your industry. Could you share more about how I could break into this field?', 26, 58, 25, 31, true),
('I`ve been thinking about doing an independent study next semester. I`d love to get your thoughts on whether this is a good idea or how it might impact my career goals.', 22, 70, 4, 20, false),
('Could you remind me about your process for mentoring? I am interested in potentially working together in the future.', 10, 48, 27, 22, true),
('I wanted to reach out to see if you know of any career fairs or networking events that could help me expand my network in the industry.', 16, 31, 24, 23, true),
('I need help understanding how to approach professional networking. Would you be open to providing any advice or recommendations on how to make connections in [industry]?', 31, 35, 29, 12, true),
('I`ve completed a few courses that align with your work. Would you be open to reviewing my resume and offering advice on how to take the next step in my career?', 30, 3, 16, 21, false),
('I have some questions about job opportunities in [industry]. Could you provide any insights into how to navigate the hiring process?', 26, 13, 32, 9, true),
('Do you have any recommendations for summer internships? I`m eager to gain experience in [specific field] and would love any guidance.', 21, 40, 9, 10, true),
('I wanted to follow up on the referral request I sent last week. Please let me know if you need any additional information.', 12, 22, 9, 25, false),
('Could we discuss my professional goals? I want to ensure I`m on the right path to achieving my long-term career objectives.', 24, 48, 19, 25, true),
('Do you think it would be beneficial for me to apply for a professional certification this summer to support my career development?', 9, 60, 8, 1, true),
('I`m considering taking an extra course next semester to support my career goals. Can you advise me on whether this is a good choice?', 35, 38, 10, 33, false),
('Can you confirm whether I`m on track with my current career plan? I want to make sure I`m focusing on the right skills for future job opportunities.', 28, 49, 29, 36, false),
('I would like to meet and discuss my professional development plan. Do you have time next week for a brief meeting?', 20, 74, 35, 7, true),
('I`m struggling to balance my current job with school. Do you have any advice on managing time effectively between work and professional development?', 3, 18, 37, 24, false),
('Could you remind me when the next networking event is? I want to make sure I don`t miss an opportunity to connect with professionals in the field.', 29, 44, 21, 6, false),
('I`m almost ready to submit my portfolio for review. Would you be willing to provide some final feedback before I send it out?', 33, 14, 22, 9, false),
('I`m considering changing industries and would love to hear your thoughts on this transition. Do you think it`s a good move given my background?', 33, 63, 1, 39, false),
('Can we meet to discuss how I can better position myself for job opportunities in the future? I would really value your input.', 20, 32, 6, 13, false),
('Can you recommend any professional organizations that could help me connect with others in the field?', 7, 41, 19, 36, true);


insert into Advisor_Messages (studentId, advisorId, content) values
(5, 23, 'Could you please clarify the requirements for the final project? I am a bit confused about the scope.'),
(16, 28, 'I have finished the reading for this week. Do you have any additional resources that could help deepen my understanding?'),
(19, 2, 'Thank you for your feedback on my paper. I will revise the thesis as suggested and get back to you shortly.'),
(36, 21, 'Just wanted to check in and see how you`re doing with the course. Let me know if you have any questions or concerns.'),
(29, 33, 'I`ve reviewed your draft. There are some points that need more development, but you`re on the right track. Let me know if you`d like to discuss further.'),
(1, 12, 'I`ll be attending the conference next week. Do you have any advice on how to make the most of it?'),
(12, 23, 'I`m running behind on the reading due to some personal matters. Is there a way to get an extension on the deadline?'),
(3, 3, 'I noticed you didn`t attend the last class. Is everything okay? Let me know if you need any assistance catching up.'),
(32, 19, 'I`m still struggling with some of the concepts from last week`s lecture. Would it be possible to meet for a brief review?'),
(32, 5, 'I`ve completed my part of the group project, but I`m waiting on the other members to submit their work. Could you follow up with them?'),
(26, 16, 'Just wanted to let you know that I submitted the assignment early. Let me know if you need anything else from me.'),
(23, 35, 'I would like to schedule an appointment to discuss my career options. Do you have any openings this week?'),
(23, 2, 'Can you help me understand the grading rubric for this course? I want to make sure I`m meeting all expectations.'),
(20, 18, 'Please let me know if I`m missing any assignments. I want to make sure I`m staying on top of things.'),
(28, 13, 'I`ve completed the extra credit work you suggested. Can you confirm if it`s been added to my grade?'),
(12, 7, 'Can you give me some feedback on my thesis draft? I`m especially unsure about the argument`s clarity.'),
(8, 39, 'I will be out of town next week for a family event. Can I submit the work ahead of time or will I be able to make it up?'),
(22, 21, 'I reviewed the syllabus again, and I still have a few questions. Can we discuss it during office hours tomorrow?'),
(32, 36, 'Is there any way I can get help with the lab experiment? I`m having trouble with the data analysis part.'),
(14, 29, 'Could you please clarify how the final grade will be calculated? I want to make sure I understand the weighting of each component.'),
(26, 23, 'I`ve sent the email to my group members about the upcoming presentation. I`ll be ready to present when the time comes.'),
(37, 3, 'I`ve looked over the course materials, and I have a question about one of the assignments. Could you explain it further?'),
(22, 12, 'I need help understanding how to approach the upcoming research project. Could we meet to go over the details?'),
(3, 2, 'I finished the assignment early. Please let me know if anything needs to be revised or if I missed something important.'),
(19, 1, 'I have some questions about the midterm exam. Can you help clarify some of the material we covered?'),
(38, 15, 'Do you have any recommendations for summer research programs? I`m interested in exploring opportunities related to my field of study.'),
(11, 34, 'I wanted to follow up on the recommendation letter request I sent last week. Please let me know if you need anything further from me.'),
(36, 24, 'Can we discuss my graduation requirements? I want to ensure that I`m on track to graduate next semester.'),
(22, 12, 'Do you think it would be beneficial for me to take a summer course to stay on track with my academic plan?'),
(33, 18, 'I`m considering taking an extra class next semester. Can you advise me on whether it`s a good idea given my current workload?'),
(34, 30, 'Can you confirm whether I`m enrolled in the right courses for my major? I want to make sure I`m on the right path.'),
(28, 7, 'I would like to meet and discuss my future career plans. Do you have time next week for a chat?'),
(3, 37, 'I`m having trouble managing my time between work and school. Do you have any strategies for staying organized?'),
(21, 18, 'Could you remind me when the next office hours are? I need to meet with you to go over some of my work.'),
(27, 37, 'I`m almost done with my thesis and would appreciate your final review before I submit it. Would you be able to look it over?'),
(28, 25, 'I`m considering changing my major. Can we discuss my options during your office hours?'),
(6, 25, 'Can we meet to discuss my final paper? I have some questions about the structure and the argument.'),
(34, 9, 'Can you recommend any scholarships or grants that I might be eligible for? I`m looking for funding opportunities.'),
(33, 39, 'I`ve sent the email to my group members about the upcoming presentation. I`ll be ready to present when the time comes.'),
(14, 4, 'Can you confirm whether I`m enrolled in the right courses for my major? I want to make sure I`m on the right path.'),
(7, 18, 'Please let me know if I`m missing any assignments. I want to make sure I`m staying on top of things.'),
(25, 25, 'Just wanted to touch base and see how things are going with the course.'),
(17, 36, 'Could you remind me when the next office hours are? I need to meet with you to go over some of my work.'),
(33, 31, 'I`m having trouble with the data analysis in the current lab experiment. Could we meet to go over it?'),
(7, 36, 'I`m considering changing my major. Can we discuss my options during your office hours?'),
(35, 9, 'Could you clarify how the grading system works? I`m not entirely sure how my work is being assessed.'),
(38, 12, 'I need help understanding the course material better. Would you be available for a tutoring session?'),
(18, 27, 'I have a question about the upcoming exam. Could we go over the material during your office hours?'),
(3, 18, 'Could you give me some feedback on my latest assignment? I want to make sure I`m on the right track.'),
(4, 37, 'I wanted to follow up on the recommendation letter request I sent last week. Please let me know if you need anything further from me.'),
(8, 40, 'I would like to meet and discuss my future career plans. Do you have time next week for a chat?'),
(36, 24, 'Just wanted to check in and see how you`re doing with the course. Let me know if you have any questions or concerns.'),
(10, 12, 'I would appreciate your input on my thesis topic. Could we set up a time to discuss it?'),
(18, 39, 'I`m thinking about pursuing an internship next summer. Do you have any advice on finding one in my field?'),
(31, 28, 'Can we schedule a time to discuss my academic progress? I`d like your feedback on my performance so far.'),
(26, 18, 'Can you review my research paper before I submit it? I would really value your feedback.'),
(20, 11, 'I need to reschedule my upcoming meeting. Could we find a new time that works for both of us?'),
(7, 7, 'I wanted to follow up on the extra credit work. Is there anything more I can do to improve my grade?'),
(19, 37, 'I`d like to meet with you to discuss my upcoming graduation. Could you advise me on the next steps?'),
(30, 17, 'Do you have any recommendations for summer research programs? I`m interested in exploring opportunities related to my field of study.'),
(15, 30, 'I have some questions about the upcoming midterm exam. Would you be able to provide more details?'),
(1, 16, 'Can you help me navigate the course requirements for next semester? I`m trying to plan ahead.'),
(5, 21, 'I would like to meet to discuss some career advice. Are there any opportunities you recommend I look into?'),
(37, 11, 'I`m wondering if you could clarify the grading process for our final project. How should we format it?'),
(39, 32, 'Could you provide more information about the upcoming class presentation? I want to ensure I`m fully prepared.');

