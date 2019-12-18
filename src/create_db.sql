PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Team_Project_rel;

DROP TABLE IF EXISTS Student_Team_rel;

DROP TABLE IF EXISTS Student_Project_rel;

DROP TABLE IF EXISTS Projects;

DROP TABLE IF EXISTS Mentors;

DROP TABLE IF EXISTS Teams;

DROP TABLE IF EXISTS Students;

DROP TABLE IF EXISTS Organisations;

DROP TABLE IF EXISTS Universities;


CREATE TABLE Organisations (
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar,
    type varchar,
    is_active boolean,
    date_added datetime
);

CREATE TABLE Universities (
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar,
    date_added integer   
);

CREATE TABLE Mentors (
    login varchar,
    password_hash varchar,
    full_name varchar,
    organisation integer,
    registration_date datetime,
    FOREIGN KEY (organisation) REFERENCES Organisations(id)
);

CREATE TABLE Students (
    login varchar,
    password_hash varchar,
    full_name varchar,
    uni_group varchar,
    university integer,
    interests varchar,
    registration_date datetime
);

CREATE TABLE Projects (
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar,
    description varchar,
    result_description varchar,
    is_active boolean,
    keywords varchar,
    mentor varchar,
    date_created datetime,
    FOREIGN KEY (mentor) REFERENCES Mentors(login)
);

CREATE TABLE Teams (
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar,
    creator varchar,
    date_created datetime,
    FOREIGN KEY (creator) REFERENCES Students(login)
);

CREATE TABLE Team_Project_rel (
    team integer,
    project integer,
    is_approved boolean,
    date_created datetime,
    PRIMARY KEY (team, project),
    FOREIGN KEY (team) REFERENCES Teams(id),
    FOREIGN KEY (project) REFERENCES Project(id)
);

CREATE TABLE Student_Team_rel (
    student varchar,
    team integer,
    is_approved integer,
    date_created datetime,
    PRIMARY KEY (student, team),
    FOREIGN KEY (student) REFERENCES Students(login),
    FOREIGN KEY (team) REFERENCES Teams(id)
);

CREATE TABLE Student_Project_rel (
    student varchar,
    project integer,
    grade integer,
    is_approved boolean,
    date_created datetime,
    PRIMARY KEY (student, project),
    FOREIGN KEY (student) REFERENCES Students(login),
    FOREIGN KEY (project) REFERENCES Project(id)
);
