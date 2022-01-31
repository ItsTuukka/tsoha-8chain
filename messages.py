from itertools import chain
from db import db
import users, chains

def get_list():
    chain_id=chains.chain_id()
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND M.chain_id=:chain_id AND M.visible=TRUE ORDER BY M.id"
    result = db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchall()

def send(content):
    visible = True
    user_id = users.user_id()
    chain_id = chains.chain_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, chain_id, user_id, sent_at, visible) VALUES (:content, :chain_id, :user_id, NOW(), :visible)"
    db.session.execute(sql, {"content":content, "chain_id":chain_id, "user_id":user_id, "visible":visible})
    db.session.commit()
    return True