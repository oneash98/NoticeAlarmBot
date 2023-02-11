CREATE DATABASE SITELOG;
USE SITELOG;

CREATE TABLE '사이트이름' (
	id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    url VARCHAR(500),
    datetime DATETIME NOT NULL,
    PRIMARY KEY (id)
);

CREATE DATABASE SUBSCRIPTION;
USE SUBSCRIPTION;

CREATE TABLE USER (
    chatid BIGINT NOT NULL,
    lastname VARCHAR(30),
    firstname VARCHAR(30),
    date_enrolled DATETIME NOT NULL,
    PRIMARY KEY (chatid)
);

CREATE TABLE WEBSITE (
    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    site_name VARCHAR(30) NOT NULL,
    url VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE SUBSCRIPTION (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    website TINYINT UNSIGNED NOT NULL,
    date_start DATETIME NOT NULL,
    chatid BIGINT NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT website FOREIGN KEY (website) REFERENCES WEBSITE (id),
    CONSTRAINT chatid FOREIGN KEY (chatid) REFERENCES USER (chatid)
);

CREATE TABLE NOTICE_LOG (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    subscription SMALLINT UNSIGNED NOT NULL,
    message_info VARCHAR(1000) NOT NULL,
    datetime DATETIME NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT subscription FOREIGN KEY (subscription) REFERENCES SUBSCRIPTION (id)
);