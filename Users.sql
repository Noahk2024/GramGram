DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    aboutme TEXT NOT NULL,
    fullname TEXT NOT NULL,
    email TEXT NOT NULL
);
