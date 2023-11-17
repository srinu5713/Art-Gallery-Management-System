CREATE TABLE `login` (
  `username` varchar(25) NOT NULL,
  `password` varchar(25) NOT NULL,
  `type` enum('Admin','Visitor') NOT NULL,
  `user_id` int AUTO_INCREMENT,
  `Name` varchar(40) NOT NULL,
  `email_id` varchar(40) DEFAULT NULL,
  `phone_number` varchar(10) NOT NULL,
  CONSTRAINT `check_ph_no` CHECK (LENGTH(`phone_number`) = 10),
  PRIMARY KEY (User_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE guide (
  Guide_ID int NOT NULL AUTO_INCREMENT,
  Name varchar(20) NOT NULL,
  Phone_number varchar(10) NOT NULL,
  rating enum('1','2','3','4','5') DEFAULT NULL,
  PRIMARY KEY (Guide_ID),
  CONSTRAINT guide_chk_1 CHECK ((LENGTH(Phone_number) = 10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE guided_tour (
  Tour_ID int NOT NULL AUTO_INCREMENT,
  Guide_ID int NOT NULL,
  booking_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tour_date date NOT NULL,
  booking_user_id int not null,
  PRIMARY KEY (Tour_ID),
  CONSTRAINT guided_tour_ibfk_1 FOREIGN KEY (Guide_ID) REFERENCES guide (Guide_ID),
  CONSTRAINT booking_user_id_ibfk_1 FOREIGN KEY (booking_user_id) REFERENCES login (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE ticket (
  Ticket_ID INT NOT NULL AUTO_INCREMENT,
  date_of_visit DATE NOT NULL,
  booking_date DATE NOT NULL,
  booking_user_id INT NOT NULL,
  PRIMARY KEY (Ticket_ID)
);


CREATE TABLE artwork (
  Artwork_ID INT NOT NULL AUTO_INCREMENT,
  Title VARCHAR(30) NOT NULL,
  Artist VARCHAR(30) NOT NULL,
  Description VARCHAR(1000),
  Published_date DATE NOT NULL,
  Type ENUM('Painting', 'Sculpture', 'Illustration', 'Figurine', 'Photograph') NOT NULL,
  img_loc VARCHAR(500) NOT NULL,
  PRIMARY KEY (Artwork_ID)
);


CREATE TABLE artwork_view (
  Ticket_ID int NOT NULL,
  Artwork_ID int NOT NULL,
  PRIMARY KEY (Ticket_ID,Artwork_ID),
  CONSTRAINT artwork_view_ibfk_1 FOREIGN KEY (Ticket_ID) REFERENCES Ticket (Ticket_ID),
  CONSTRAINT artwork_view_ibfk_2 FOREIGN KEY (Artwork_ID) REFERENCES artwork (Artwork_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE visitor_tag (
  Tag_ID int NOT NULL AUTO_INCREMENT,
  Ticket_ID int DEFAULT NULL,
  Assigned_Date date NOT NULL,
  PRIMARY KEY (Tag_ID),
  CONSTRAINT visitor_tag_ibfk_1 FOREIGN KEY (Ticket_ID) REFERENCES  Ticket(Ticket_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE review (
  Review_ID int NOT NULL AUTO_INCREMENT,
  Artwork_ID int NOT NULL,
  username varchar(25) NOT NULL,
  rating enum('1','2','3','4','5') NOT NULL,
  comment varchar(100) DEFAULT 'N/A',
  Review_date date NOT NULL DEFAULT (CURRENT_DATE),
  PRIMARY KEY (Review_ID),
  CONSTRAINT review_ibfk_1 FOREIGN KEY (Artwork_ID) REFERENCES artwork (Artwork_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE visitor_transactions (
  Trans_ID int NOT NULL AUTO_INCREMENT,
  Booking_User_ID int NOT NULL,
  No_of_Tickets int NOT NULL,
  Time timestamp NULL DEFAULT NULL,
  PRIMARY KEY (Trans_ID),
  CONSTRAINT visitor_transactions_ibfk_1 FOREIGN KEY (Booking_User_ID) REFERENCES login(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `login` (
  `username`,
  `password`,
  `type`,
  `user_id`,
  `Name`,
  `email_id`,
  `phone_number`
)
VALUES
  ('Admin', 'pass', 'Admin', 0 , 'Admin', NULL, '9724238431'),
  ('Arun', 'vis1', 'Visitor', 1, 'Arun', 'amouli@example.com', '9715497891'),  -- Replace with actual values
  ('Priyanka', 'vis0', 'Visitor', 4, 'Priyanka', 'DongrePriya@example.com', '7804521457'),  -- Replace with actual values
  ('Rahul', 'vis7', 'Visitor', 3, 'Rahul', 'rsharma@example.com', '7654789145'),  -- Replace with actual values
  ('Surya', 'vis2', 'Visitor', 2, 'Surya', 'svardhan@example.com', '8765487109');


INSERT INTO guide (Name, Phone_number, rating)
VALUES
    ('Rajesh Kumar', '9876543210', '4'),
    ('Priya Sharma', '8765432109', '5'),
    ('Amit Singh', '7654321098', '3'),
    ('Sanya Verma', '6543210987', '2'),
    ('Vikas Patel', '5432109876', '4');

INSERT INTO guided_tour (Guide_ID, booking_time, tour_date, booking_user_id, slot)
VALUES
  (1, '2023-11-12 12:28:24', '2023-11-10', 6, 1),
  (2, '2023-11-12 12:28:24', '2023-11-11', 7, 1),
  (3, '2023-11-12 12:28:24', '2023-11-12', 8, 1),
  (4, '2023-11-12 12:28:24', '2023-11-13', 9, 1),
  (5, '2023-11-12 12:28:24', '2023-11-14', 10, 1);



INSERT INTO `ticket` (`Ticket_ID`,  `date_of_visit`, `booking_date`)
VALUES
  (1, '2023-11-10', '2023-11-09'),
  (2, '2023-11-11', '2023-11-10'),
  (3, '2023-11-12', '2023-11-11'),
  (4, '2023-11-13', '2023-11-12'),
  (5, '2023-11-14', '2023-11-13');

INSERT INTO artwork (Artwork_ID, Title, Artist, description, Published_date, Type, img_loc)
VALUES
  (20, 'Mona Lisa', 'Leonardo da Vinci', 'Famous portrait', '1972-03-23', 'Painting', 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/483px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg'),
  (21, 'The Starry Night', 'Vincent van Gogh', 'Impressionist painting', '1980-02-29', 'Painting', 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/the starry night.jpg'),
  (22, 'The Thinker', 'Auguste Rodin', 'Bronze sculpture', '2011-07-03', 'Sculpture', 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/thinker.jpg'),
  (23, 'Saurashtra', 'Sayed Haider Raza', 'Abstract art', '2016-06-15', 'Illustration', 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/Saurashtra.jpg'),
  (24, 'Indian Heritage', 'Raja Ravi Varma', 'Classical Indian art', '2002-09-11', 'Painting', 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/Indian Heritage.jpg'),
  (25, 'Krishna Wall Art', 'Raja Ravi Verma', 'Krishna paintings often employ symbolism and metaphor to convey deeper meanings. The peacock feather in Krishna\'s crown symbolizes beauty and grace, while the flute represents divine music and harmony.', '2017-07-13', 'Illustration', 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/-473Wx593H-464518099-multi-MODEL.jpg');


INSERT INTO `artwork_view` (`Ticket_ID`, `Artwork_ID`)
VALUES
  (5, 1),
  (1, 2),
  (2, 2),
  (3, 4),
  (4, 4);


INSERT INTO `visitor_tag` (`Ticket_ID`, `Assigned_Date`)
VALUES
  (1, '2023-11-10'),
  (2, '2023-11-11'),
  (3, '2023-11-12'),
  (4, '2023-11-13'),
  (5, '2023-11-14');


INSERT INTO review (Review_ID, Artwork_ID, username, rating, comment, Review_date)
VALUES
  (1, 20, 'Arun', 5, 'Amazing artwork!', '2023-11-10'),
  (2, 21, 'Priyanka', 4, 'Love the colors!', '2023-11-11'),
  (3, 22, 'Surya', 3, 'Interesting sculpture', '2023-11-12'),
  (4, 23, 'Priyanka', 2, 'Not my style', '2023-11-13'),
  (5, 24, 'Rahul', 4, 'Beautiful depiction of Indian heritage', '2023-11-14');



INSERT INTO `visitor_transactions` (`Booking_User_ID`, `No_of_Tickets`, `Time`)
VALUES
  (6, 2, '2023-11-09 08:30:00'),
  (8, 1, '2023-11-12 11:15:00'),
  (9, 2, '2023-11-13 12:00:00');







