CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN, visible BOOLEAN);

CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, user_id INTEGER REFERENCES users, sent_at TIMESTAMP, visible BOOLEAN);