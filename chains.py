from db import db
import users

def get_list(t_id):
    sql = "SELECT id, description, topic_id, user_id FROM chains WHERE topic_id=:t_id AND visible=TRUE"
    result = db.session.execute(sql, {"t_id":t_id})
    return result.fetchall()

def create_chain(chainname):
    visible = True
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO chains (description, topic_id, user_id, creted_at, visible) VALUES (:chainname, :topic_id, :user_id, NOW() :visible)"
    db.session.execute(sql, {"chainname":chainname, "user_id":user_id, "visible":visible})
    db.session.commit()
    return True