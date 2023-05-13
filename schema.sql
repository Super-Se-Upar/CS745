DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies(
    comp_name TEXT PRIMARY KEY,
    coi INTEGER NOT NULL
);

CREATE TABLE users (
    emp_id TEXT PRIMARY KEY,
    emp_password TEXT NOT NULL,
    emp_role TEXT NOT NULL,
    companies TEXT NOT NULL
);


CREATE TABLE files (
    file_name TEXT PRIMARY KEY,
    file_cont TEXT NOT NULL,
    sanitized BOOLEAN NOT NULL,
    cd TEXT NOT NULL
);