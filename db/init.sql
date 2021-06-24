CREATE SCHEMA IF NOT EXISTS sudoku;

CREATE TABLE IF NOT EXISTS servers
(
  -- using 32 as id len to future-proof
  id varchar(32) PRIMARY KEY,
  prefix varchar(5) DEFAULT 'su!'
);

CREATE
USER bot WITH PASSWORD 'bot';
GRANT SELECT, INSERT, UPDATE, DELETE
    ON servers
    TO bot;