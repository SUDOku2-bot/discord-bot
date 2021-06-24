#!/bin/bash

set -e

sudo docker-compose up &

psql -v ON_ERROR_STOP=1 --username sudokudev --dbname sudokudev <<-EOSQL
  CREATE TABLE IF NOT EXISTS servers
  (
      -- using 32 as id len to future-proof
      id varchar(32) PRIMARY KEY,
      prefix varchar(5) DEFAULT 'su!'
  );
EOSQL
