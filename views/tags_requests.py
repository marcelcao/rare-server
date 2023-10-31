import sqlite3
import json
from models import Tag

def get_all_tags():
    """Fetches all tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        """)

        tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])
            tags.append(tag.__dict__)

    return tags

def get_single_tag(id):
    """Variable to hold a single tag if it exists"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        tag = Tag(data['id'], data['label'])

        return tag.__dict__

def create_tag(new_tag):
    """Creates a new tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?);
        """, (new_tag['label'],))

        id = db_cursor.lastrowid
        new_tag['id'] = id


    return new_tag

def delete_tag(id):
    """Function to delete a tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Tags
        WHERE id = ?
        """, (id, ))

def update_tag(id, new_tag):
    """Updates tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?
        """, (new_tag['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def get_tag_by_label(label):
    """Query for customer email address"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.label
        from Tags t
        WHERE t.label = ?
        """, ( label, ))

        labels = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            label = Tag(row['id'], row['label'])
            labels.append(label.__dict__)

    return labels
