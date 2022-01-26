from db import db
import users

def get_list(t_id):
    sql = "SELECT description, topic_id, users_id, FROM chains WHERE topic_id={t_id} visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()