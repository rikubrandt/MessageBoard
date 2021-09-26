--Needs to have atleast 1 account created

INSERT INTO boards (id, name, moderator) VALUES (1, 'Random', 1);
INSERT INTO boards (id, name, moderator) VALUES (2, 'Stoopid', 1);
INSERT INTO boards (id, name, moderator) VALUES (3, 'SQL', 1);

INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'Is random random?', NOW(), 1);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'Is there random?', NOW(), 1);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'Is those random?', NOW(), 1);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'Is them random?', NOW(), 2);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'Is that random?', NOW(), 2);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'Is this random?', NOW(), 3);


INSERT INTO messages (post_id, user_id, content, sent_at) VALUES (1, 1, 'My first post', NOW());
INSERT INTO messages (post_id, user_id, content, sent_at) VALUES (2, 1, 'My sec post', NOW());
INSERT INTO messages (post_id, user_id, content, sent_at) VALUES (3, 1, 'My 34d post', NOW());
INSERT INTO messages (post_id, user_id, content, sent_at) VALUES (3, 1, 'My 3123 post', NOW());
INSERT INTO messages (post_id, user_id, content, sent_at) VALUES (4, 1, 'My firasdst post', NOW());
INSERT INTO messages (post_id, user_id, content, sent_at) VALUES (4, 1, 'My dasd post', NOW());
