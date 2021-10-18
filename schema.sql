DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS boards CASCADE;

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    role_id integer REFERENCES roles(id)
);

CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT,
    moderator integer REFERENCES users(id),
    visible boolean default true
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    post_owner integer REFERENCES users(id),
    title TEXT,
    created_at TIMESTAMP,
    board integer REFERENCES boards(id),
    visible boolean default true
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    post_id integer REFERENCES posts(id),
    user_id integer REFERENCES users(id), 
    content TEXT,
    created_at TIMESTAMP,
    visible boolean default true
);

INSERT INTO roles(role_name) VALUES ('USER');
INSERT INTO roles(role_name) VALUES ('MODERATOR');
INSERT INTO roles(role_name) VALUES ('ADMIN');