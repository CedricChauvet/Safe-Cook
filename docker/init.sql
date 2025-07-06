CREATE DATABASE IF NOT EXISTS safecook;
USE safecook;

-- 1. Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

-- 2. Table des allergies (valeurs possibles)
CREATE TABLE IF NOT EXISTS allergies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Table de liaison user ↔ allergies
CREATE TABLE IF NOT EXISTS user_allergies (
  user_id INT NOT NULL,
  allergy_id INT NOT NULL,
  PRIMARY KEY (user_id, allergy_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (allergy_id) REFERENCES allergies(id) ON DELETE CASCADE
);



INSERT INTO allergies (id, name) VALUES
  (1, 'Gluten'),
  (2, 'Lactose'),
  (3, 'Arachides'),
  (4, 'Vegetarien');



-- Insérer des utilisateurs fictifs
INSERT INTO users (email, password) VALUES
  ('alice@example.com', 'password123'),
  ('bob@example.com', 'password456');

-- Associer les utilisateurs à leurs allergies
-- On suppose que Gluten = id 1, Lactose = id 2
INSERT INTO user_allergies (user_id, allergy_id) VALUES
  (1, 1), -- Alice allergique au Gluten
  (1, 2), -- Alice allergique au Lactose
  (2, 2); -- Bob allergique au Lactose