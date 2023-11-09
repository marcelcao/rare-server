import sqlite3
import json
from models import PostReaction, Reaction

def get_all__post_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.reaction_id,
            a.user_id,
            a.post_id
        FROM postreactions a
        """)

        postreactions = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post_reaction = PostReaction(row['id'],
                                         row['reaction_id'], row['user_id'], row['post_id'])

            postreactions.append(post_reaction.__dict__)

    return postreactions

def get_single_post_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
           a.id,
           a.reaction_id,
           a.user_id,
           a.post_id
        FROM postreactions a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        post_reaction = PostReaction(data['id'],
                                     data['reaction_id'], data['user_id'], data['post_id'])
        return post_reaction.__dict__
    

def get_post_reactions_by_post_id(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.reaction_id,
            a.user_id,
            a.post_id,
            r.id,
            r.label,
            r.image_url
        FROM postreactions a
        JOIN reactions r
            ON r.id = a.reaction_id
        WHERE post_id = ?
        """, ((id), ))

        postreactions = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post_reaction = PostReaction(row['id'],
                                         row['reaction_id'], row['user_id'], row['post_id'])
            
            reaction = Reaction(row['id'], row['label'], row['image_url'])
            
            post_reaction.reaction = reaction.__dict__
            postreactions.append(post_reaction.__dict__)

    return postreactions
        


def create_post_reaction(new_post_reaction):
    with sqlite3.connect("./db.sqlite3") as conn:

        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostReactions
            (reaction_id, user_id, post_id )
        VALUES
            ( ?, ?, ?);
        """, (new_post_reaction['reaction_id'],
              new_post_reaction['user_id'], new_post_reaction['post_id'], ))

        id = db_cursor.lastrowid
        new_post_reaction['id'] = id

        return new_post_reaction


def delete_post_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM postreactions
        WHERE id = ?
        """, (id, ))


def update_post_reaction(id, new_post_reaction):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE PostReactions
            SET
                reaction_id = ?,
                user_id = ?,
                post_id = ?
        WHERE id = ?
        """, (new_post_reaction['reaction_id'],
              new_post_reaction['user_id'], new_post_reaction['post_id'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
