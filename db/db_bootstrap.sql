-- This file is to bootstrap a database for the CS3200 project. 
drop database Chart;
-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database Chart;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on Chart.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 
use Chart;

-- Put your DDL
CREATE TABLE Artist (
    username VARCHAR(20) PRIMARY KEY,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    stageName varchar(255) NOT NULL,
    country varchar(255) NOT NULL,
    dateJoined DATE DEFAULT NOW(),
    phone VARCHAR(10) UNIQUE,
    email varchar(255) UNIQUE,
    genre varchar(255),
    dayRank INT UNIQUE DEFAULT NULL,
    monthRank INT UNIQUE DEFAULT NULL,
    weekRank INT UNIQUE DEFAULT NULL,
    totalDislikes INT DEFAULT 0,
    totalLikes INT DEFAULT 0,
    dateOfBirth DATE
);

CREATE TABLE User (
    username VARCHAR(20) PRIMARY KEY,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    country varchar(255) NOT NULL,
    dateJoined DATE,
    phone INTEGER(10),
    email varchar(255) NOT NULL,
    dateOfBirth DATE
);

CREATE TABLE RecordLabel (
    companyID VARCHAR(20) PRIMARY KEY,
    name varchar(255) NOT NULL UNIQUE,
    contactFirstName varchar(255) NOT NULL,
    contactLastName varchar(255) NOT NULL,
    dateJoined DATE,
    billingStreetAddress varchar(255),
    billingCityAddress varchar(255),
    billingStateAddress varchar(255),
    billingCountryAddress varchar(255),
    headquartersStreetAddress varchar(255),
    headquartersCityAddress varchar(255),
    headquartersStateAddress varchar(255),
    headquartersCountryAddress varchar(255),
    contactPhone INTEGER(10) NOT NULL,
    contactEmail varchar(255) NOT NULL
);

CREATE TABLE Song (
    songID VARCHAR(20) PRIMARY KEY,
    genre varchar(255) NOT NULL,
    language varchar(255) NOT NULL,
    title varchar(255) NOT NULL,
    duration INT,
    dateReleased DATE,
    dayRank INT,
    monthRank INT,
    weekRank INT,
    dislikes INT DEFAULT 0,
    likes INT DEFAULT 0,
    artistUsername varchar(20) NOT NULL,
    CONSTRAINT fk_song_to_artist FOREIGN KEY (artistUsername) REFERENCES Artist (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE SongCatalog (
    catalogID VARCHAR(20) PRIMARY KEY,
    totalSales INT,
    value INT,
    genre varchar(255) NOT NULL,
    name VARCHAR(20) NOT NULL,
    companyID VARCHAR(20),
    songID VARCHAR(20),
    CONSTRAINT fk_catalog_record_label FOREIGN KEY (companyID) REFERENCES RecordLabel (companyID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_catalog_song FOREIGN KEY (songID) REFERENCES Song (songID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Researcher (
    researcherID VARCHAR(20) PRIMARY KEY,
    institution varchar(255) NOT NULL,
    dataUsed FLOAT,
    dateJoined DATETIME DEFAULT NOW(),
    contactFirstName varchar(255) NOT NULL,
    contactLastName varchar(255) NOT NULL,
    contactPhone INTEGER(10) NOT NULL,
    contactEmail varchar(255) NOT NULL
);

CREATE TABLE Signings (
    artistUsername VARCHAR(20),
    companyID VARCHAR(20),
    CONSTRAINT fk_signings_artist FOREIGN KEY (artistUsername) REFERENCES Artist (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_signings_company FOREIGN KEY (companyID) REFERENCES RecordLabel (companyID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE SongLikes (
    songID VARCHAR(20),
    userUsername VARCHAR(20),
    CONSTRAINT fk_likes_user FOREIGN KEY (userUsername) REFERENCES User (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_likes_song FOREIGN KEY (songID) REFERENCES Song (songID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE ResearcherViews (
    researcherID VARCHAR(20),
    userUsername VARCHAR(20),
    CONSTRAINT fk_research_user FOREIGN KEY (userUsername) REFERENCES User (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_research_researcher FOREIGN KEY (researcherID) REFERENCES Researcher (researcherID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE ArtistFollows (
    artistUsername VARCHAR(20),
    userUsername VARCHAR(20),
    CONSTRAINT fk_follows_artist FOREIGN KEY (artistUsername) REFERENCES Artist (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_follows_user FOREIGN KEY (userUsername) REFERENCES User (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Friends (
    requestUsername VARCHAR(20),
    acceptUsername VARCHAR(20),
    CONSTRAINT fk_friends_req FOREIGN KEY (requestUsername) REFERENCES User (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_friends_acc FOREIGN KEY (acceptUsername) REFERENCES User (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


-- Add sample data.
DELETE FROM Artist;

INSERT INTO Artist (username, firstName, lastName, stageName, country, dateJoined, phone, email, genre, dayRank, monthRank, weekRank, totalDislikes, totalLikes, dateOfBirth)
VALUE ('davidzhang0', 'David', 'Zhang', 'davidz', 'USA', NOW(), 6316379598, 'dzhang.og@gmail.com', 'jazz', 1, 1, 1, 0, 0, NOW());