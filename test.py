import pymongo
from pymongo import MongoClient
from user_data_handler import *

client = MongoClient("mongodb+srv://mongouser:O6TYkZnXi39z@cluster0.fapa8.mongodb.net/client.test?retryWrites=true&w=majority")
db = client['test']
posts = db.posts

post = {
	"telegram_id": 358904540,
	"photo_id": 'none',
	"name": 'none',
	"company": 'none',
	"lfwhat": 'none',
	"skills": 'none',
	"active": 'none',
	"nickname": 'none',
	"bot_state": 'awaiting_photo_full' 
}
# posts.insert_one(post)
# posts.delete_one({"telegram_id": str(358904540)})
# posts.delete_one({"telegram_id": 358904540})
print(posts.find_one({"telegram_id": 358904540}))

