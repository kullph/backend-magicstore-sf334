CREATE TABLE Users (
    ID SERIAL PRIMARY KEY,
    Firstname VARCHAR(255),
    Lastname VARCHAR(255),
    Point INT
);

CREATE TABLE Authen (
    ID SERIAL PRIMARY KEY,
    User_ID INT,
    Email VARCHAR(255),
    Password VARCHAR(255),
    FOREIGN KEY (User_ID) REFERENCES Users(ID)
);

CREATE TABLE Product (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT,
    Img_path TEXT,
    Price FLOAT,
    Left_Quantity INT,
    Sales_Quantity INT
);

CREATE TABLE Cart (
    ID SERIAL PRIMARY KEY,
    User_ID INT,
    Product_ID INT,
    Quantity INT,
    FOREIGN KEY (User_ID) REFERENCES Users(ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(ID)
);

CREATE TABLE Ordered (
    ID SERIAL PRIMARY KEY,
    User_ID INT,
    Product_ID INT,
    Quantity INT,
    OrderDate TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(ID)
);

CREATE TABLE Delivery_source (
    ID SERIAL PRIMARY KEY,
    User_ID INT,
    Detail TEXT,
    Phone VARCHAR(255),
    Province VARCHAR(255),
    District VARCHAR(255),
    Subdistrict VARCHAR(255),
    Zipcode VARCHAR(255),
    FOREIGN KEY (User_ID) REFERENCES Users(ID)
);

CREATE TABLE Review (
    ID SERIAL PRIMARY KEY,
    User_ID INT,
    Product_ID INT,
    Detail TEXT,
    Score INT,
    FOREIGN KEY (User_ID) REFERENCES Users(ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(ID)
);

CREATE TABLE Category (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255)
);

CREATE TABLE Element (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Product_ID INT,
    FOREIGN KEY (Product_ID) REFERENCES Product(ID)
);


CREATE TABLE Action (
    ID SERIAL PRIMARY KEY,
    action VARCHAR(255),
    time TIMESTAMP
);

CREATE TABLE Status (
    ID SERIAL PRIMARY KEY,
    Action_ID INT,
    status VARCHAR(255),
    FOREIGN KEY (Action_ID) REFERENCES Action(ID)
);