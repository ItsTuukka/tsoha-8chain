from db import db
import users, chains, topics

def get_list():
    chain_id=chains.chain_id()
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND M.chain_id=:chain_id AND M.visible=TRUE ORDER BY M.id"
    result = db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchall()

def send(content):
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

def validate_msg(content):
    if not content or len(content) < 3 or len(content) > 5000:
        return False
    return True