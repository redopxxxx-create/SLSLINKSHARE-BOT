from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import OWNER_ID, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time

# Yeh part comment out hi rehne dete hain taaki bot har message pe reply na kare
"""
@Bot.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)
"""

@Bot.on_message(filters.command('stats') & filters.user(OWNER_ID))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    
    # Hinglish UI for stats
    stats_msg = f"<b>📊 SLS BOT STATUS</b>\n\n<b>🚀 Uptime:</b> {time}\n<b>👤 Owner:</b> <a href='tg://user?id={OWNER_ID}'>Admin</a>\n\n<i>Bot ekdum mast chal raha hai! ✅</i>"
    
    await message.reply(stats_msg)

# +++ Modified By @itsryosudhish [SLS Bots] +++
# Logic maintained for interconnected system stability.
