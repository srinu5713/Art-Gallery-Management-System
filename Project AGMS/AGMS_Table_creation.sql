CREATE DATABASE AGMS;

USE AGMS

CREATE TABLE Ticket(Ticket_ID int PRIMARY KEY, date_of_visit date NOT NULL,booking_date date NOT NULL);


CREATE TABLE Visitor (Visitor_ID int PRIMARY KEY,Ticket_ID int NOT NULL,Name varchar(30) NOT NULL,Email_ID varchar(40),Phone_Number varchar(10) NOT NULL,FOREIGN KEY (Ticket_ID) REFERENCES Ticket (Ticket_ID),CHECK (LENGTH(Phone_Number) = 10));

CREATE TABLE Visitor_Log(Log_ID int PRIMARY KEY, Visitor_ID int,entry_time timestamp NOT NULL,exit_time timestamp NOT NULL,FOREIGN KEY(Visitor_ID) REFERENCES Visitor(Visitor_ID));

CREATE TABLE Visitor_tag(Tag_ID int PRIMARY KEY, Visitor_ID int,Assigned_Date date NOT NULL,FOREIGN KEY(Visitor_ID) REFERENCES Visitor(Visitor_ID));


CREATE TABLE Guide(Guide_ID int PRIMARY KEY, Name varchar(20) NOT NULL,Phone_number varchar(10) NOT NULL,rating enum('1','2','3','4','5'),CHECK (LENGTH(Phone_number) = 10));

CREATE TABLE Guided_tour(Tour_ID int PRIMARY KEY,Guide_ID int NOT NULL,booking_time timestamp NOT NULL DEFAULT NOW(),tour_date date NOT NULL, FOREIGN KEY(Guide_ID) REFERENCES Guide(Guide_ID));


CREATE TABLE Artwork(Artwork_ID int PRIMARY KEY,Title varchar(30) NOT NULL,Artist varchar(30) NOT NULL,description varchar(100),Published_date date NOT NULL);

CREATE TABLE Review(Review_ID int PRIMARY KEY,Artwork_ID int,Visitor_ID int,rating enum('1','2','3','4','5'), comment varchar(100) DEFAULT 'N/A',Review_date date NOT NULL DEFAULT(CURRENT_DATE));


CREATE TABLE Artwork_view(Visitor_ID int,Artwork_ID int,PRIMARY KEY(Visitor_ID,Artwork_ID));



visitor_log
visitor_tag
review
artwork_view
artwork_log
visitor_transactions



CREATE TABLE visitor (
  Visitor_ID int NOT NULL ,
  Ticket_ID int NOT NULL,
 
  PRIMARY KEY (Visitor_ID),
  CONSTRAINT visitor_ibfk_1 FOREIGN KEY (Ticket_ID) REFERENCES ticket (Ticket_ID),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
