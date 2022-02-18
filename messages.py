from db import db
import users, chains, topics, validate

def get_list():
    chain_id=chains.chain_id()
    sql = "SELECT M.content, U.username, M.sent_at, M.user_id, M.id FROM messages M, users U WHERE M.user_id=U.id AND M.chain_id=:chain_id AND M.visible=TRUE ORDER BY M.id"
    result = db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchall()

def send(content):
    if not validate.msg(content):
        return False
    topic_id = topics.topic_id()
    user_id = users.user_id()
    chain_id = chains.chain_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, topic_id, chain_id, user_id, sent_at, visible) VALUES (:content, :topic_id, :chain_id, :user_id, NOW(), TRUE)"
    db.session.execute(sql, {"content":content, "topic_id":topic_id, "chain_id":chain_id, "user_id":user_id})
    db.session.commit()
    topics.update_messages_count()
    return True

def get_latest_message(topic_id):
    sql = "SELECT sent_at FROM messages WHERE topic_id=:topic_id AND visible=TRUE ORDER BY id DESC"
    result = db.session.execute(sql, {"topic_id":topic_id})
    date = result.fetchone()
    return date[0]

def updatemsg(content, id):
    if not validate.msg(content):
        return False
    try:
        sql = "UPDATE messages SET content=:content WHERE id=:id"
        db.session.execute(sql, {"content":content, "id":id})
        db.session.commit()
        return True
    except:
        return False

def get_likes(msg_id):
    sql = "SELECT COUNT (*) FROM likes WHERE message_id=:msg_id"
    result = db.session.execute(sql, {"msg_id":msg_id})
    likes = result.fetchone()
    return likes[0]
    
def add_like(msg_id):
    sql = "INSERT INTO likes (message_id, user_id) VALUES (:msg_id, :user_id)"
    db.session.execute(sql, {"msg_id":msg_id, "user_id":users.user_id()})
    db.session.commit()

def get_filtered_messages(filter):
    print(filter)
    sql = "SELECT M.content, U.username, M.sent_at, M.chain_id, M.id FROM messages M, users U WHERE M.content LIKE :filter AND M.user_id=U.id AND M.visible=TRUE ORDER BY M.id"
    result = db.session.execute(sql, {"filter":"%"+filter+"%"})
    return result.fetchall()