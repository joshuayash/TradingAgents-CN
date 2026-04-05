#!/usr/bin/env python3
"""创建默认用户脚本"""
import sys
sys.path.insert(0, '/app')

import asyncio
import hashlib
from datetime import datetime
from pymongo import MongoClient

# MongoDB 连接
MONGO_URI = "mongodb://mongo:uuKzGrOMrhonqBraXYoGlAzhRPQcHscH@mongodb.railway.internal:27017/tradingagents?authSource=admin"
DB_NAME = "tradingagents"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_users():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    users_collection = db.users
    
    # 检查是否已存在 admin 用户
    existing = users_collection.find_one({"username": "admin"})
    if existing:
        print("✓ admin 用户已存在")
        client.close()
        return
    
    # 创建管理员用户
    admin_user = {
        "username": "admin",
        "email": "admin@tradingagents.cn",
        "hashed_password": hash_password("admin123"),
        "is_active": True,
        "is_verified": True,
        "is_admin": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None,
        "preferences": {
            "default_market": "A股",
            "default_depth": "深度",
            "ui_theme": "light",
            "language": "zh-CN",
            "notifications_enabled": True,
            "email_notifications": False
        }
    }
    
    users_collection.insert_one(admin_user)
    print("✅ 管理员用户创建成功")
    print("   用户名: admin")
    print("   密码: admin123")
    
    # 创建测试用户
    test_user = {
        "username": "test",
        "email": "test@tradingagents.cn",
        "hashed_password": hash_password("test123"),
        "is_active": True,
        "is_verified": True,
        "is_admin": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None,
        "preferences": {
            "default_market": "A股",
            "default_depth": "标准",
            "ui_theme": "light",
            "language": "zh-CN",
            "notifications_enabled": True,
            "email_notifications": False
        }
    }
    
    users_collection.insert_one(test_user)
    print("✅ 测试用户创建成功")
    print("   用户名: test")
    print("   密码: test123")
    
    client.close()

if __name__ == "__main__":
    create_users()
