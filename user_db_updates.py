# downloadable imports:
import sqlite3


def update_photo(user_id, PhotoId):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM users WHERE UserId = {user_id}''')
    if not c.fetchone():
        conn.close()
        return 0
    c.execute(f'''UPDATE users SET PhotoId = "{PhotoId}" WHERE UserId = {user_id}''')
    conn.commit()
    conn.close()
    return 1


def update_name_and_surname(user_id, name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM users WHERE UserId = {user_id}''')
    if not c.fetchone():
        conn.close()
        return 0
    c.execute(f'''UPDATE users SET Name = "{name}" WHERE UserId = {user_id}''')
    conn.commit()
    conn.close()
    return 1


def update_lfwhat(user_id, lfwhat_text):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM users WHERE UserId = {user_id}''')
    if not c.fetchone():
        conn.close()
        return 0
    c.execute(f'''UPDATE users SET LfWhat = "{lfwhat_text}" WHERE UserId = {user_id}''')
    conn.commit()
    conn.close()
    return 1


def update_skills(user_id, skills_text):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM users WHERE UserId = {user_id}''')
    if not c.fetchone():
        conn.close()
        return 0
    c.execute(f'''UPDATE users SET Skills = "{skills_text}" WHERE UserId = {user_id}''')
    conn.commit()
    conn.close()
    return 1


def update_company(user_id, company_text):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM users WHERE UserId = {user_id}''')
    if not c.fetchone():
        conn.close()
        return 0
    c.execute(f'''UPDATE users SET Company = "{company_text}" WHERE UserId = {user_id}''')
    conn.commit()
    conn.close()
    return 1


def update_active(user_id, active_text):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM users WHERE UserId = {user_id}''')
    if not c.fetchone():
        conn.close()
        return 0
    c.execute(f'''UPDATE users SET Active = "{active_text}" WHERE UserId = {user_id}''')
    conn.commit()
    conn.close()
    return 1