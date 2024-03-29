from db import db
import users

def get_posts(topic_id):
    sql = "SELECT id, user_id, title FROM posts WHERE topic_id=:topic_id AND visible=TRUE"
    return db.session.execute(sql, {"topic_id": topic_id}).fetchall()

def get_post_info(post_id):
    sql = "SELECT P.id, P.topic_id, P.user_id, U.username, P.title, P.content, T.private, P.visible FROM posts P " \
          "INNER JOIN users U ON P.user_id=U.id INNER JOIN topics T ON P.topic_id=T.id " \
          "WHERE P.id=:post_id"
    return db.session.execute(sql, {"post_id": post_id}).fetchone()

def get_op(post_id):
    sql = "SELECT user_id FROM posts WHERE id=:post_id"
    return db.session.execute(sql, {"post_id": post_id}).fetchone()

def get_user_post_count(user_id):
    sql = "SELECT COUNT(*) FROM posts WHERE user_id=:user_id AND visible=TRUE"
    return db.session.execute(sql, {"user_id": user_id}).fetchone()

def add_post(topic_id, title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO posts (topic_id, user_id, title, content) VALUES (:topic_id, :user_id, :title, :content)"
    db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id, "title": title, "content": content})
    db.session.commit()
    return True

def update_post(post_id, content):
    user_id = users.user_id()
    if user_id == 0 or user_id != get_op(post_id)[0]:
        return False
    sql = "UPDATE posts SET content=:content WHERE id=:post_id"
    db.session.execute(sql, {"post_id": post_id, "content": content})
    db.session.commit()
    return True

def delete_post(post_id):
    user_id = users.user_id()
    if not users.is_admin:
        if user_id == 0 or user_id != get_op(post_id)[0]:
            return False
    sql = "UPDATE posts SET visible=FALSE WHERE id=:post_id; " \
          "DELETE FROM comments C USING posts P WHERE C.post_id=P.id AND P.visible=FALSE"
    db.session.execute(sql, {"post_id": post_id})
    db.session.commit()
    return True

def search_posts(word):
    sql = "SELECT P.id, P.title, T.private FROM posts P INNER JOIN topics T ON P.topic_id=T.id " \
          "WHERE P.title ILIKE :word AND T.private=FALSE AND P.visible=TRUE"
    return db.session.execute(sql, {"word": "%"+word+"%"}).fetchall()
