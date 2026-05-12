# +++ Modified By @itsryosudhish [SLS Bots] +++

import motor.motor_asyncio
import base64
from config import DB_URI, DB_NAME
from datetime import datetime, timedelta
from typing import List, Optional

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

# collections
user_data = database['users']
channels_collection = database['channels']
fsub_channels_collection = database['fsub_channels']

# --- User Management ---
async def add_user(user_id: int) -> bool:
    if not isinstance(user_id, int) or user_id <= 0: return False
    try:
        existing_user = await user_data.find_one({'_id': user_id})
        if existing_user: return False
        await user_data.insert_one({'_id': user_id, 'created_at': datetime.utcnow()})
        return True
    except: return False

async def present_user(user_id: int) -> bool:
    return bool(await user_data.find_one({'_id': user_id}))

async def full_userbase() -> List[int]:
    return [doc['_id'] async for doc in user_data.find()]

async def del_user(user_id: int) -> bool:
    result = await user_data.delete_one({'_id': user_id})
    return result.deleted_count > 0

# --- Admin Management ---
async def is_admin(user_id: int) -> bool:
    admins_collection = database['admins']
    try:
        return bool(await admins_collection.find_one({'_id': int(user_id)}))
    except: return False

async def add_admin(user_id: int) -> bool:
    admins_collection = database['admins']
    try:
        await admins_collection.update_one({'_id': int(user_id)}, {'$set': {'_id': int(user_id)}}, upsert=True)
        return True
    except: return False

async def remove_admin(user_id: int) -> bool:
    result = await database['admins'].delete_one({'_id': int(user_id)})
    return result.deleted_count > 0

async def list_admins() -> list:
    admins = await database['admins'].find().to_list(None)
    return [admin['_id'] for admin in admins]

# --- Channel & Link Management ---
async def save_channel(channel_id: int) -> bool:
    try:
        await channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"channel_id": channel_id, "status": "active", "created_at": datetime.utcnow()}},
            upsert=True
        )
        return True
    except: return False

async def get_channels() -> List[int]:
    channels = await channels_collection.find({"status": "active"}).to_list(None)
    return [ch["channel_id"] for ch in channels if "channel_id" in ch]

async def delete_channel(channel_id: int) -> bool:
    result = await channels_collection.delete_one({"channel_id": channel_id})
    return result.deleted_count > 0

async def save_encoded_link(channel_id: int) -> Optional[str]:
    try:
        encoded_link = base64.urlsafe_b64encode(str(channel_id).encode()).decode()
        await channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"encoded_link": encoded_link, "status": "active"}},
            upsert=True
        )
        return encoded_link
    except: return None

async def get_channel_by_encoded_link(encoded_link: str) -> Optional[int]:
    channel = await channels_collection.find_one({"encoded_link": encoded_link, "status": "active"})
    return channel["channel_id"] if channel else None

async def save_encoded_link2(channel_id: int, encoded_link: str) -> Optional[str]:
    try:
        await channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"req_encoded_link": encoded_link, "status": "active"}},
            upsert=True
        )
        return encoded_link
    except: return None

async def get_channel_by_encoded_link2(encoded_link: str) -> Optional[int]:
    channel = await channels_collection.find_one({"req_encoded_link": encoded_link, "status": "active"})
    return channel["channel_id"] if channel else None

# --- Invite & Approval Logic ---
async def save_invite_link(channel_id: int, invite_link: str, is_request: bool) -> bool:
    try:
        await channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"current_invite_link": invite_link, "is_request_link": is_request, "invite_link_created_at": datetime.utcnow()}},
            upsert=True
        )
        return True
    except: return False

async def get_current_invite_link(channel_id: int) -> Optional[dict]:
    channel = await channels_collection.find_one({"channel_id": channel_id})
    if channel and "current_invite_link" in channel:
        return {"invite_link": channel["current_invite_link"], "is_request": channel.get("is_request_link", False)}
    return None

async def get_link_creation_time(channel_id: int):
    channel = await channels_collection.find_one({"channel_id": channel_id})
    return channel.get("invite_link_created_at") if channel else None

async def get_original_link(channel_id: int) -> Optional[str]:
    channel = await channels_collection.find_one({"channel_id": channel_id})
    return channel.get("original_link") if channel else None

async def set_approval_off(channel_id: int, off: bool = True) -> bool:
    try:
        await channels_collection.update_one({"channel_id": channel_id}, {"$set": {"approval_off": off}}, upsert=True)
        return True
    except: return False

async def is_approval_off(channel_id: int) -> bool:
    channel = await channels_collection.find_one({"channel_id": channel_id})
    return bool(channel and channel.get("approval_off", False))

# --- FSub Logic ---
async def get_fsub_channels() -> List[int]:
    channels = await fsub_channels_collection.find({'status': 'active'}).to_list(None)
    return [ch['channel_id'] for ch in channels]
