import sqlite3
import json
from models.post import Post

def get_all_posts():
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content
        FROM Posts a    
        """
        # JOIN user u
        # ON u.id = a.user_id
        # JOIN category c
        # ON c.id = a.category_id
        )
        
        posts = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'])
            
            # adds user and category to post
            # user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], user['password'], row['profile_image_url'], row['created_on'])
            # category = Category(row['id'], row['label'])
            # post.user = user.__dict__
            # post.category = category.__dict__
            
            posts.append(post.__dict__)
        
        return posts

def get_single_post(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content
        FROM posts a
        WHERE a.id = ?                  
        """, (id, ))
        
        # FROM post a
        # JOIN user u
        # ON u.id = a.user_id
        # JOIN category c
        # ON c.id = a.category_id
        
        data = db_cursor.fetchone()
        
        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'])
        
        return post.__dict__

def get_posts_by_user_id(user_id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content
        FROM posts a
        WHERE a.user_id = ?                  
        """, (user_id))
        
        posts = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'])
            posts.append(post.__dict__)
            
        return posts

def create_post(new_post):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO posts
            (user_id, category_id, title, publication_date, image_url, content)
        VALUES
            (?, ?, ?, ?, ?, ?)                  
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content']))
        
        id = db_cursor.lastrowid
        
        new_post['id'] = id
        
    return new_post

def update_post(id, new_post):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], id, ))

        rows_affected = db_cursor.rowcount
        
        if rows_affected == 0:
            return False
        else:
            return True
        
def delete_post(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?                  
        """, (id,))
