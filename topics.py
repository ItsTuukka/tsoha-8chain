from db import db
import users

def get_list():
    sql = "SELECT id, topicname FROM topics WHERE visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def create_topic(topicname):
    visible = True
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO topics (topicname, visible) VALUES (:topicname, :visible)"
    db.session.execute(sql, {"topicname":topicname, "visible":visible})
    db.session.commit()
    return True

