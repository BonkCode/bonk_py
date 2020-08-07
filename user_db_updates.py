# downloadable imports:
import pymongo
from pymongo import MongoClient

client = MongoClient("")
db = client['test']
posts = db.posts

# posts.update_one({"telegram_id": user_id}, {"$set": {"bot_state": state_text}})
def update_photo(user_id, PhotoId):
	if not posts.find_one({"telegram_id": user_id}):
		return 0
	posts.update_one({"telegram_id": user_id}, {"$set": {"photo_id": PhotoId}})
	return 1


def update_name_and_surname(user_id, name):
	if not posts.find_one({"telegram_id": user_id}):
		return 0
	posts.update_one({"telegram_id": user_id}, {"$set": {"name": name}})
	return 1


def update_lfwhat(user_id, lfwhat_text):
	if not posts.find_one({"telegram_id": user_id}):
		return 0
	posts.update_one({"telegram_id": user_id}, {"$set": {"lfwhat": lfwhat_text}})
	return 1


def update_skills(user_id, skills_text):
	if not posts.find_one({"telegram_id": user_id}):
		return 0
	posts.update_one({"telegram_id": user_id}, {"$set": {"skills": skills_text}})
	return 1


def update_company(user_id, company_text):
	if not posts.find_one({"telegram_id": user_id}):
		return 0
	posts.update_one({"telegram_id": user_id}, {"$set": {"company": company_text}})
	return 1


def update_active(user_id, active_text):
	if not posts.find_one({"telegram_id": user_id}):
		return 0
	posts.update_one({"telegram_id": user_id}, {"$set": {"active": active_text}})
	return 1
