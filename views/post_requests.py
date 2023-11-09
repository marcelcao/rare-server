import sqlite3
import json
from .comment_requests import get_comments_by_post_id
from .post_reaction_requests import get_post_reactions_by_post_id
from models.post import Post
from models.user import User
from models.comment import Comment


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
            a.content,
            u.username,
            u.profile_image_url,
            u.first_name,
            u.last_name,
            u.id,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Posts a
        JOIN users u
            ON u.id = a.user_id
        """
        )
        
        
        posts = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['title'], row['publication_date'], row['image_url'], row['content'])
            post_author = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            post.author = post_author.get_username_and_id()
            
            # get assosciated comments section
            post_comments = get_comments_by_post_id(row['id'])
            post.comments = post_comments
            post_reactions = get_post_reactions_by_post_id(row['id'])
            post.post_reactions = post_reactions
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
            a.content,
            u.username,
            u.profile_image_url,
            u.first_name,
            u.last_name,
            u.id,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM posts a
        JOIN users u
            ON u.id = a.user_id
        WHERE a.id = ?
        """, (id, ))
        
        
        
        # FROM post a
        # post_tags = get_posttags_by_post_id(id)
        
        
        
        data = db_cursor.fetchone()
        
        post = Post(data['id'], data['user_id'], data['title'], data['publication_date'], data['image_url'], data['content'])
        author = User(data['user_id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'])
        post.author = author.get_username_and_id()
        
        comments = get_comments_by_post_id(data['id'])
        post.comments = comments
        post_reactions = get_post_reactions_by_post_id(data['id'])
        post.post_reactions = post_reactions
        # post.post_tags = post_tags
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
            post = Post(row['id'], row['user_id'], row['title'], row['publication_date'], row['image_url'], row['content'])
            posts.append(post.__dict__)
            
        return posts

def create_post(new_post):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO posts
            (user_id, title, publication_date, image_url, content)
        VALUES
            (?, ?, ?, ?, ?)                  
        """, (new_post['user_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content']))
        
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
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], id, ))

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
