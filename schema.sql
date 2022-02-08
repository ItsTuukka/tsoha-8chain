CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT, 
    admin BOOLEAN, 
    visible BOOLEAN);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY, 
    topicname TEXT UNIQUE,
    chains INTEGER, 
    messages INTEGER, 
    visible BOOLEAN);

CREATE TABLE chains (
    id SERIAL PRIMARY KEY, 
    description TEXT, 
    topic_id INTEGER REFERENCES topics, 
    user_id INTEGER REFERENCES users, 
    created_at TIMESTAMP, 
    visible BOOLEAN);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY, 
    content TEXT,
    topic_id INTEGER REFERENCES topics, 
    chain_id INTEGER REFERENCES chains,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP, 
    visible BOOLEAN);