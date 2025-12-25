from pymongo import MongoClient
from config import MONGO_URI

# Database connection
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["N4_Bots"]
users_collection = db["users_sequence"]

# Data storage (global variables)
user_sequences = {}
user_notification_msg = {}
update_tasks = {}
user_settings = {} 
processing_users = set()  # 🔥 ADDED: To prevent multiple "Processing" messages
user_ls_state = {}  # NEW: Store LS command state
user_mode = {}  # NEW: Store user mode (file or caption)

def get_user_stats(user_id):
    """Get user statistics from database"""
    return users_collection.find_one({"user_id": user_id})

def update_user_stats(user_id, files_count, username):
    """Update user statistics in database"""
    users_collection.update_one(
        {"user_id": user_id}, 
        {"$inc": {"files_sequenced": files_count}, "$set": {"username": username}}, 
        upsert=True
    )

def get_top_users(limit=5):
    """Get top users by files sequenced"""
    return users_collection.find().sort("files_sequenced", -1).limit(limit)

def get_total_users():
    """Get total number of users"""
    return users_collection.count_documents({})

def get_all_users():
    """Get all users for broadcasting"""
    return list(users_collection.find({}))

def save_broadcast_stats(total, success, failed, blocked):
    """Save broadcast statistics"""
    from datetime import datetime
    db.broadcast_stats.update_one(
        {"_id": "latest"},
        {
            "$set": {
                "total": total,
                "success": success,
                "failed": failed,
                "blocked": blocked,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        },
        upsert=True
    )

# NEW: Get user mode
def get_user_mode(user_id):
    """Get user mode (default is 'file' if not set)"""
    return user_mode.get(user_id, "file")

# NEW: Set user mode
def set_user_mode(user_id, mode):
    """Set user mode ('file' or 'caption')"""
    if mode in ["file", "caption"]:
        user_mode[user_id] = mode
        return True
    return False
