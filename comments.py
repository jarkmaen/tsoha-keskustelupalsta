from db import db
import users

def get_comments(post_id):
    sql = "SELECT C.id AS comment_id, U.id AS user_id, U.username, C.content FROM comments C " \
          "INNER JOIN users U ON C.user_id=U.id WHERE C.post_id=:post_id ORDER BY C.id ASC"
    return db.session.execute(sql, {"post_id": post_id}).fetchall()

def get_commenter(comment_id):
    sql = "SELECT user_id FROM comments WHERE id=:comment_id"
    return db.session.execute(sql, {"comment_id": comment_id}).fetchone()

def get_user_comment_count(user_id):
    sql = "SELECT COUNT(*) FROM comments WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id": user_id}).fetchone()

def get_user_comment_history(user_id):
    sql = "SELECT C.post_id, P.title, C.content FROM comments C " \
          "INNER JOIN posts P ON C.post_id=P.id WHERE C.user_id=:user_id AND P.visible=TRUE"
    return db.session.execute(sql, {"user_id": user_id}).fetchall()

def add_comment(post_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (post_id, user_id, content) VALUES (:post_id, :user_id, :content)"
    db.session.execute(sql, {"post_id": post_id, "user_id": user_id, "content": content})
    db.session.commit()
    return True

def update_comment(comment_id, content):
    user_id = users.user_id()
    if user_id == 0 or user_id != get_commenter(comment_id)[0]:
        return False
    sql = "UPDATE comments SET content=:content WHERE id=:comment_id;"
    db.session.execute(sql, {"comment_id": comment_id, "content": content})
    db.session.commit()
    return True

def delete_comment(comment_id):
    user_id = users.user_id()
    if not users.is_admin:
        if user_id == 0 or user_id != get_commenter(comment_id)[0]:
            return False
    sql = "DELETE FROM comments WHERE id=:comment_id"
    db.session.execute(sql, {"comment_id": comment_id})
    db.session.commit()
    return True
