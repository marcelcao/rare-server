import sqlite3
import json
from models import Comment

COMMENTS = [
  {
    "id": 1,
    "author_id": "Zack",
    "post_id": 4,
    "content": "Neat post!"
  },
  {
    "id": 2,
    "author_id": "Jimmy",
    "post_id": 1,
    "content": "Awful post!"
  }
]

def get_all_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.author_id,
            a.post_id,
            a.content
        FROM comments a
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['author_id'], row['post_id'],
                            row['content'])

            comments.append(comment.__dict__) # see the notes below for an explanation on this line of code.

        return comments
  
def get_single_comment(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.author_id,
            a.post_id,
            a.content
        FROM comments a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        comment = Comment(data['id'], data['author_id'], data['post_id'],
                            data['content'])

        return comment.__dict__
      
def create_comment(new_comment):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO comments
            (author_id, post_id, content)
        VALUES
            (?, ?, ?)                  
        """, (new_comment['author_id'], new_comment['post_id'], new_comment['content']))
        
        id = db_cursor.lastrowid
        
        new_comment['id'] = id
        
    return new_comment

def update_comment(id, new_comment):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE comments
            SET
                author_id = ?,
                post_id = ?,
                content = ?
        WHERE id = ?
        """, (new_comment['author_id'], new_comment['post_id'], new_comment['content'], id, ))

        rows_affected = db_cursor.rowcount
        
        if rows_affected == 0:
            return False
        else:
            return True

def delete_comment(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?                  
        """, (id,))
