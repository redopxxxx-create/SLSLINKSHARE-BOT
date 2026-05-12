# +++ Modified By @itsryosudhish [SLS Bots] +++
# Original Logic by Codeflix Bots

import os
import asyncio
from config import *
from pyrogram import Client, filters
from pyrogram.types import Message, User
from pyrogram.errors import FloodWait, ChatAdminRequired, RPCError
from database.database import add_admin, remove_admin, list_admins

# Command to Add Admin (Only Owner can use)
@Client.on_message(filters.command("addadmin") & filters.user(OWNER_ID))
async def add_admin_command(client, message: Message):
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("<b>Usage:</b> <code>/addadmin {user_id}</code>")
    
    user_id = int(message.command[1])
    success = await add_admin(user_id)
    
    if success:
        await message.reply_text(f"<b>✅ User <code>{user_id}</code> ko Admin bana diya gaya hai!</b>")
    else:
        await message.reply_text(f"<b>❌ Kuch gadbad hui! Admin add nahi ho paya.</b>")

# Command to Delete Admin (Only Owner can use)
@Client.on_message(filters.command("deladmin") & filters.user(OWNER_ID))
async def del_admin_command(client, message: Message):
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("<b>Usage:</b> <code>/deladmin {user_id}</code>")
    
    user_id = int(message.command[1])
    success = await remove_admin(user_id)
    
    if success:
        await message.reply_text(f"<b>✅ User <code>{user_id}</code> ko Admin list se hata diya gaya hai.</b>")
    else:
        await message.reply_text(f"<b>❌ Error: User admin list mein nahi mila.</b>")

# Command to List All Admins
@Client.on_message(filters.command("admins") & filters.user(OWNER_ID))
async def list_admins_command(client, message: Message):
    admins = await list_admins()
    
    if not admins:
        return await message.reply_text("<b>Abhi tak koi admin set nahi kiya gaya hai. 🧐</b>")
    
    text = "<b>👑 SLS BOT ADMIN LIST:</b>\n\n"
    text += "\n".join([f"🔹 <code>{uid}</code>" for uid in admins])
    text += "\n\n<i>Sirf Owner hi admins manage kar sakta hai.</i>"
    
    await message.reply_text(text)
