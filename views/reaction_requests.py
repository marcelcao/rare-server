import sqlite3
import json
from models import Reaction

def get_all_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.label,
            a.image_url
        FROM reactions a
        """)

        reactions = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            reaction = Reaction(row['id'], row['label'], row['image_url'])

            reactions.append(reaction.__dict__)

    return reactions

def get_single_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
           a.id,
           a.label,
           a.image_url
        FROM reactions a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        reaction = Reaction(data['id'], data['label'], data['image_url'])

        return reaction.__dict__


def create_reaction(new_reaction):
    with sqlite3.connect("./db.sqlite3") as conn:

        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO reactions
            ( label, image_url)
        VALUES
            ( ?, ?);
        """, (new_reaction['label'], new_reaction['image_url'], ))

        id = db_cursor.lastrowid
        new_reaction['id'] = id

    return new_reaction


def delete_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM reactions
        WHERE id = ?
        """, (id, ))


def update_reaction(id, new_reaction):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Reactions
            SET
                label = ?,
                image_url = ?
                
        WHERE id = ?
        """, (new_reaction['label'], new_reaction['image_url'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
