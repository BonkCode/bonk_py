# downloadable imports:
import sqlite3


def get_photo_id(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT PhotoId FROM users WHERE UserId = {user_id}''')
    return_value = c.fetchone()
    conn.close()
    return return_value[0]


def get_name(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT Name FROM users WHERE UserId = {user_id}''')
    return_value = c.fetchone()
    conn.close()
    return return_value[0]


def get_company(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT Company FROM users WHERE UserId = {user_id}''')
    return_value = c.fetchone()
    conn.close()
    return return_value[0]


def get_lfwhat(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT LfWhat FROM users WHERE UserId = {user_id}''')
    return_value = c.fetchone()
    conn.close()
    return return_value[0]


def get_skills(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT Skills FROM users WHERE UserId = {user_id}''')
    return_value = c.fetchone()
    conn.close()
    return return_value[0]
