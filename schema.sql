CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    role integer NOT NULL DEFAULT '1'
)

CREATE TABLE room (
    id integer PRIMARY KEY,
    name TEXT,
    moderator integer REFERENCES users(user_id),

)

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    post_owner integer REFERENCES users(id)
    title TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    post_id integer REFERENCES posts(post_id),
    user_id integer REFERENCES users(id), 
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
