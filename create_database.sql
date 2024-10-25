CREATE DATABASE IF NOT EXISTS `flaskapp-database`;

CREATE TABLE IF NOT EXISTS `flaskapp-database`.`students` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);
