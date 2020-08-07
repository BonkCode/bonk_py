# downloadable imports:
import pymongo
from pymongo import MongoClient
# local imports:
from state import State

client = MongoClient("")
db = client['test']
posts = db.posts

def update_state(user_id, state_text):
	posts.update_one({"telegram_id": user_id}, {"$set": {"bot_state": state_text}})



def get_state(user_id):
	fetch = posts.find_one({"telegram_id": user_id})
	if not fetch:
		return None
	bot_state = State(fetch.get('telegram_id'), fetch.get('bot_state'))
	print (bot_state.state_text)
	return bot_state
