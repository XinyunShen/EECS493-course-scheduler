PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40),
  filename VARCHAR(64),
  password VARCHAR(256),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(username)
);

CREATE TABLE schedule(
  username VARCHAR(20) NOT NULL,
  courseid INTEGER NOT NULL,
  timeid INTEGER NOT NULL,
  PRIMARY KEY(username, timeid)
);

CREATE TABLE course(
  courseid INTEGER NOT NULL,
  credits INTEGER NOT NULL,
  coursename VARCHAR(20) NOT NULL,
  description VARCHAR(500) NOT NULL,
  prerequisite VARCHAR(64),
  PRIMARY KEY(courseid)
);

CREATE TABLE coursetime(
  courseid INTEGER NOT NULL,
  timeid INTEGER NOT NULL,
  starttime TIME NOT NULL,
  endtime TIME NOT NULL,
  weekday VARCHAR(256),
  PRIMARY KEY(courseid, timeid)
);

CREATE TABLE following(
  username1 VARCHAR(20) NOT NULL,
  username2 VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY(username1, username2),
  FOREIGN KEY(username1) REFERENCES users(username)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(username2) REFERENCES users(username)
  ON UPDATE CASCADE ON DELETE CASCADE
);
