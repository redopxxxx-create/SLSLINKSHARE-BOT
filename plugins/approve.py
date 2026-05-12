# +++ Modified By @itsryosudhish [SLS Bots] +++
# Original Logic by Yato (@ProYato)
# aNDI BANDI SANDI JISNE BHI CREDIT HATAYA USKI BANDI RAndi 

import os
import asyncio
from config import *
from pyrogram import Client, filters
from pyrogram.types import Message, User, ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, ChatAdminRequired, RPCError, UserNotParticipant
from database.database import set_approval_off, is_approval_off
from helper_func import *

# Default settings
APPROVAL_WAIT_TIME = 5  
AUTO_APPROVE_ENABLED = True  

@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client, message: ChatJoinRequest):
    global AUTO_APPROVE_ENABLED

    if not AUTO_APPROVE_ENABLED:
        return

    chat = message.chat
    user = message.from_user

    # Check agar approval off hai is channel ke liye
    if await is_approval_off(chat.id):
        print(f"Auto-approval is OFF for channel {chat.id}")
        return

    # Thoda wait karenge system stability ke liye
    await asyncio.sleep(APPROVAL_WAIT_TIME)

    try:
        # Approval process start
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        
        if APPROVED == "on":
            # SLS Bots Style Hinglish Message
            buttons = [
                [InlineKeyboardButton('• Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ •', url='https://t.me/Starlight_Animes')],
                [InlineKeyboardButton(f'• Jᴏɪɴ {chat.title} •', url=f'https://t.me/{chat.username}' if chat.username else 'https://t.me/Starlight_Animes')]
            ]
            markup = InlineKeyboardMarkup(buttons)
            
            caption = (
                f"<b>Oye {user.mention}! 👋\n\n"
                f"Aapki join request <u>{chat.title}</u> ke liye approve ho gayi hai. ✅\n\n"
                f"Maze karo aur updates ke liye channel join rakho!</b>"
            )
            
            await client.send_photo(
                chat_id=user.id,
                photo=START_PIC, # Config se image uthayega
                caption=caption,
                reply_markup=markup
            )
    except Exception as e:
        print(f"Approval Error: {e}")

# --- ADMIN COMMANDS (Hinglish UI) ---

@Client.on_message(filters.command("reqtime") & is_owner_or_admin)
async def set_reqtime(client, message: Message):
    global APPROVAL_WAIT_TIME
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("<b>Usage:</b> <code>/reqtime 10</code> (seconds mein)")
    
    APPROVAL_WAIT_TIME = int(message.command[1])
    await message.reply_text(f"✅ Ab approval wait time <b>{APPROVAL_WAIT_TIME}</b> seconds set kar diya gaya hai.")

@Client.on_message(filters.command("reqmode") & is_owner_or_admin)
async def toggle_reqmode(client, message: Message):
    global AUTO_APPROVE_ENABLED
    if len(message.command) != 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply_text("<b>Usage:</b> <code>/reqmode on/off</code>")
    
    mode = message.command[1].lower()
    AUTO_APPROVE_ENABLED = (mode == "on")
    status = "CHALU ✅" if AUTO_APPROVE_ENABLED else "BAND ❌"
    await message.reply_text(f"Auto-approval system ab <b>{status}</b> hai.")

@Client.on_message(filters.command("approveoff") & is_owner_or_admin)
async def approve_off_command(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("<b>Usage:</b> <code>/approveoff Channel_ID</code>")
    
    channel_id = int(message.command[1])
    await set_approval_off(channel_id, True)
    await message.reply_text(f"✅ Channel <code>{channel_id}</code> ke liye auto-approval <b>OFF</b> kar di gayi hai.")

@Client.on_message(filters.command("approveon") & is_owner_or_admin)
async def approve_on_command(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("<b>Usage:</b> <code>/approveon Channel_ID</code>")
    
    channel_id = int(message.command[1])
    await set_approval_off(channel_id, False)
    await message.reply_text(f"✅ Channel <code>{channel_id}</code> ke liye auto-approval wapas <b>ON</b> kar di gayi hai.")
