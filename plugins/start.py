
import asyncio
import base64
import time
from asyncio import Lock
from collections import defaultdict
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatMemberStatus, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors import FloodWait, UserNotParticipant, UserIsBlocked, InputUserDeactivated
import os
import random 

from bot import Bot
from datetime import datetime, timedelta
from config import *
from database.database import *
from plugins.newpost import revoke_invite_after_5_minutes
from helper_func import *

# Create a lock dictionary for each channel
channel_locks = defaultdict(asyncio.Lock)
user_banned_until = {}

# --- HINGLISH UI TEXTS ---
WELCOME_TEXT = "**Kaise ho {mention}! 👋**\n\nMain ek advanced **Link Sharing Bot** hoon. Mere saath aap apne links secure rakh sakte ho.\n\nNiche diye gaye buttons check karein! 👇"

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Bot, message: Message):
    user_id = message.from_user.id

    # Anti-Spam Check (Original)
    if user_id in user_banned_until:
        if datetime.now() < user_banned_until[user_id]:
            return await message.reply_text(
                "<b>Sabar rakho bro! Thodi der baad try karna. ⏳</b>",
                parse_mode=ParseMode.HTML
            )
            
    await add_user(user_id)

    # ✅ Check Force Subscription (Hinglish UI Integrated)
    if not await is_subscribed(client, message):
        return

    text = message.text
    if len(text) > 7:
        # --- Original Link Fetching Logic Start ---
        try:
            base64_string = text.split(" ", 1)[1]
            is_request = base64_string.startswith("req_")
            
            if is_request:
                base64_string = base64_string[4:]
                channel_id = await get_channel_by_encoded_link2(base64_string)
            else:
                channel_id = await get_channel_by_encoded_link(base64_string)
            
            if not channel_id:
                return await message.reply_text("<b>Invalid Link ya expire ho chuka hai. 😕</b>")

            from database.database import get_original_link
            original_link = await get_original_link(channel_id)
            if original_link:
                button = InlineKeyboardMarkup([[InlineKeyboardButton("• Proceed to Link •", url=original_link)]])
                return await message.reply_text("<b>Aapka link niche hai! Click karke aage badhein. ✅</b>", reply_markup=button)

            async with channel_locks[channel_id]:
                old_link_info = await get_current_invite_link(channel_id)
                current_time = datetime.now()
                
                if old_link_info:
                    link_created_time = await get_link_creation_time(channel_id)
                    if link_created_time and (current_time - link_created_time).total_seconds() < 240:
                        invite_link = old_link_info["invite_link"]
                        is_request_link = old_link_info["is_request"]
                    else:
                        try:
                            await client.revoke_chat_invite_link(channel_id, old_link_info["invite_link"])
                        except: pass
                        invite = await client.create_chat_invite_link(chat_id=channel_id, expire_date=current_time + timedelta(minutes=10), creates_join_request=is_request)
                        invite_link = invite.invite_link
                        is_request_link = is_request
                        await save_invite_link(channel_id, invite_link, is_request_link)
                else:
                    invite = await client.create_chat_invite_link(chat_id=channel_id, expire_date=current_time + timedelta(minutes=10), creates_join_request=is_request)
                    invite_link = invite.invite_link
                    is_request_link = is_request
                    await save_invite_link(channel_id, invite_link, is_request_link)

            button_text = "• ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ •" if is_request_link else "• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •"
            button = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=invite_link)]])

            await message.reply_text("<b>Link ready hai! Click karke join karein. 🚀</b>", reply_markup=button)
            
            note_msg = await message.reply_text("<u><b>Note: Link expire ho jaye toh wapas post link pe click karna.</b></u>")
            asyncio.create_task(delete_after_delay(note_msg, 300))
            asyncio.create_task(revoke_invite_after_5_minutes(client, channel_id, invite_link, is_request_link))

        except Exception as e:
            await message.reply_text("<b>Kuch gadbad ho gayi hai! ❌</b>")
            print(f"Error: {e}")
        # --- Original Link Fetching Logic End ---
    else:
        # Main Start UI (Hinglish)
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• About", callback_data="about"),
             InlineKeyboardButton("• Channels", callback_data="channels")],
            [InlineKeyboardButton("• Close •", callback_data="close")]
        ])
        
        await message.reply_photo(
            photo=START_PIC,
            caption=WELCOME_TEXT.format(mention=message.from_user.mention),
            reply_markup=inline_buttons
        )

# --- Credits & Callbacks Maintain Rakhe Gaye Hain ---
# @CodeFlix_Bots & @rohit_1888 original credits preserved

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data  
    
    if data == "close":
        await query.message.delete()
    
    elif data == "about":
        await query.edit_message_media(
            InputMediaPhoto("https://envs.sh/Wdj.jpg", ABOUT_TXT),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• Back', callback_data='home')]])
        )

    elif data == "channels":
        await query.edit_message_media(
            InputMediaPhoto("https://envs.sh/Wdj.jpg", CHANNELS_TXT),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• Back', callback_data='home')]])
        )
    
    elif data in ["start", "home"]:
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• About", callback_data="about"),
             InlineKeyboardButton("• Channels", callback_data="channels")],
            [InlineKeyboardButton("• Close •", callback_data="close")]
        ])
        await query.edit_message_media(
            InputMediaPhoto(START_PIC, WELCOME_TEXT.format(mention=query.from_user.mention)),
            reply_markup=inline_buttons
        )

# Helper function for auto-delete
def delete_after_delay(msg, delay):
    async def inner():
        await asyncio.sleep(delay)
        try: await msg.delete()
        except: pass
    return inner()
