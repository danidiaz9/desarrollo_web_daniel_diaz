
CREATE USER IF NOT EXISTS 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';

FLUSH PRIVILEGES;