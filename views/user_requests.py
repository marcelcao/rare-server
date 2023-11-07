import sqlite3
import json
from datetime import datetime
from models import User

def get_all_users():
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        """)
        
        users = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            user = User(row['id'],row['first_name'],row['last_name'],row['email'],row['bio'],row['username'],row['password'],row['profile_image_url'],row['created_on'],row['active'])
            
            users.append(user.__dict__)
        return users
        
def get_single_user(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Users u
        WHERE u.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        
        user = User(data['id'],data['first_name'],data['last_name'],data['email'],data['bio'],data['username'],data['password'],data['profile_image_url'],data['created_on'],data['active'])
        
        return user.__dict__      

def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })

def update_user(id, new_user):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                bio = ?,
                username = ?,
                password = ?,
                profile_image_url = ?,
                created_on = ?,
                active = ?
        WHERE id = ?
        """, (new_user['first_name'],new_user['last_name'],new_user['email'],new_user['bio'],new_user['username'],new_user['password'],new_user['profile_image_url'],new_user['created_on'],new_user['active'], id, ))
        
        rows_affected = db_cursor.rowcount
        
        if rows_affected == 0:
            return False
        else:
            return True
        
def delete_user(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Users
        WHERE id = ?
        """, (id,))        