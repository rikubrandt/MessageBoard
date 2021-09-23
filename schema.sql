DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS room CASCADE; 
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS messages CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    role integer NOT NULL DEFAULT '1'
);

CREATE TABLE boards (
    id integer PRIMARY KEY,
    name TEXT,
    moderator integer REFERENCES users(id)

);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    post_owner integer REFERENCES users(id),
    title TEXT,
    created_at TIMESTAMP,
    board integer REFERENCES boards(id)
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    post_id integer REFERENCES posts(id),
    user_id integer REFERENCES users(id), 
    content TEXT,
    sent_at TIMESTAMP
);
