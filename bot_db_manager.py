# downloadable imports:
import sqlite3
# local imports:
from state import State


def update_state(user_id, state_text, bot_message_text):
    stateconn = sqlite3.connect('bot_state.db')
    statec = stateconn.cursor()
    statec.execute(f'''SELECT * FROM states WHERE UserId = {user_id}''')
    if statec.fetchone():
        statec.execute(f'''UPDATE states SET State="{state_text}", LastBotMessage = "{bot_message_text}" WHERE UserId = {user_id}''')
        stateconn.commit()
        stateconn.close()
        return
    statec.execute(f'''INSERT INTO states VALUES ('{user_id}', '{state_text}', '{bot_message_text}')''')
    stateconn.commit()
    stateconn.close()


def get_state(user_id):
    stateconn = sqlite3.connect('bot_state.db')
    statec = stateconn.cursor()
    statec.execute(f'''SELECT * FROM states WHERE UserId = {user_id}''')
    fetch = statec.fetchone()
    if not fetch:
        update_state(user_id, 'error', 'none')
    bot_state = State(fetch[0], fetch[1], fetch[2])
    stateconn.close()
    return bot_state