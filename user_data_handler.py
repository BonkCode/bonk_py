# downloadable imports:
import pymongo
from pymongo import MongoClient

client = MongoClient("")
db = client['test']
posts = db.posts


def get_photo_id(user_id):
    return posts.find_one({"telegram_id": user_id}).get('photo_id')


def get_name(user_id):
    return posts.find_one({"telegram_id": user_id}).get('name')


def get_company(user_id):
    return posts.find_one({"telegram_id": user_id}).get('company')


def get_lfwhat(user_id):
    return posts.find_one({"telegram_id": user_id}).get('lfwhat')


def get_skills(user_id):
    return posts.find_one({"telegram_id": user_id}).get('skills')
