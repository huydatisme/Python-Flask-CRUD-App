-- create_database.sql

CREATE DATABASE IF NOT EXISTS flaskapp_database;

USE flaskapp_database;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL
);
