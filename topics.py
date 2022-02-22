from db import db
from flask import session
import validate, users

def get_list():
    sql = "SELECT id, topicname FROM topics WHERE visible=TRUE AND secret=FALSE ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_secret_list():
    if users.user_admin():
        sql = "SELECT id, topicname FROM topics WHERE visible=TRUE AND secret=TRUE ORDER BY id"
        result = db.session.execute(sql)
    else:
        sql = "SELECT id, topicname FROM topics, access WHERE id=topic_id AND user_id=:u_id AND visible=TRUE AND secret=TRUE ORDER BY id"
        result = db.session.execute(sql, {"u_id":users.user_id()})
    return result.fetchall()

def create_topic(topicname, secret):
    if not validate.topic(topicname):
        return False
    sql = "INSERT INTO topics (topicname, secret, visible) VALUES (:topicname, :secret, TRUE)"
    db.session.execute(sql, {"topicname":topicname, "secret":secret})
    db.session.commit()
    return True
    
def get_chain_count(id):
    sql = "SELECT COUNT (*) FROM chains WHERE topic_id=:id and visible=TRUE"
    result = db.session.execute(sql, {"id":id})
    count = result.fetchone()
    return count[0]

def get_message_count(id):
    sql = "SELECT COUNT (*) FROM messages WHERE topic_id=:id and visible=TRUE"
    result = db.session.execute(sql, {"id":id})
    count = result.fetchone()
    return count[0]

def get_topic_name():
    sql = "SELECT topicname FROM topics WHERE id=:t_id"
    result = db.session.execute(sql, {"t_id":topic_id()})
    name = result.fetchone()
    return name[0]

def delete(id):
    sql = "UPDATE topics SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def add_member(username, topic_id):
    usernames = users.get_usernames()
    if username not in usernames:
        return False
    user_id = users.id_from_username(username)
    if users.user_access(user_id, topic_id):
        return False
    sql = "INSERT INTO access VALUES (:topic_id, :user_id)"
    db.session.execute(sql, { "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

def set_topic_id(id):
    session['topic_id'] = id

def topic_id():
    return session.get("topic_id")


