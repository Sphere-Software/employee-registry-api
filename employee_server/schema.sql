-- Initialise the database.
-- Drop any existing data and create empty tables.
DROP TABLE IF EXISTS employee_types;
DROP TABLE IF EXISTS teams;

CREATE TABLE employee_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE teams (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

INSERT INTO
  employee_types (id, name)
VALUES
  (1, "Full time"),
  (2, "Part time"),
  (3, "Contractor");
