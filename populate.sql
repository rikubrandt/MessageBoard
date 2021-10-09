--Needs to have atleast 1 account created




INSERT INTO boards (id, name, moderator) VALUES (1, 'Random', 1);
INSERT INTO boards (id, name, moderator) VALUES (2, 'Stoopid', 1);
INSERT INTO boards (id, name, moderator) VALUES (3, 'SQL', 1);

INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'POSTIs random random?', NOW(), 1);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'POSTIs there random?', NOW(), 1);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'IPOSTIss those random?', NOW(), 1);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'POSTIs them random?', NOW(), 2);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'POSTIs that random?', NOW(), 2);
INSERT INTO posts (post_owner, title, created_at, board) VALUES (1, 'POSTIs this random?', NOW(), 3);


INSERT INTO messages (post_id, user_id, content, created_at) VALUES (1, 1, 'My first message', NOW());



INSERT INTO messages (post_id, user_id, content, created_at) VALUES (2, 1, 'My sec message', NOW());
INSERT INTO messages (post_id, user_id, content, created_at) VALUES (3, 1, 'My 34d posmessaget', NOW());
INSERT INTO messages (post_id, user_id, content, created_at) VALUES (3, 1, 'My 3123 message', NOW());
INSERT INTO messages (post_id, user_id, content, created_at) VALUES (4, 1, 'My firasdst message', NOW());
INSERT INTO messages (post_id, user_id, content, created_at) VALUES (4, 1, 'My dasd message', NOW());
