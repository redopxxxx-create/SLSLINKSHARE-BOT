# +++ Modified By Ryo [telegram username: @itsryosudhish] +++ # aNDI BANDI SANDI JISNE BHI CREDIT HATAYA USKI BANDI RAndi 
import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import ADMINS, FORCE_SUB_CHANNEL # Config se FORCE_SUB_CHANNEL import kiya
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.filters import Filter
from config import OWNER_ID
from database.database import is_admin

class IsAdmin(Filter):
    async def __call__(self, client, message):
        return await is_admin(message.from_user.id)

is_admin_filter = IsAdmin()

class IsOwnerOrAdmin(Filter):
    async def __call__(self, client, message):
        user_id = message.from_user.id
        return user_id == OWNER_ID or await is_admin(user_id)

is_owner_or_admin = IsOwnerOrAdmin()

# --- FORCE SUB LOGIC (Hinglish UI) ---
async def is_subscribed(client, message):
    if not FORCE_SUB_CHANNEL:
        return True
    try:
        user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
        if user.status == ChatMemberStatus.BANNED:
            await message.reply_text("Sorry bro, aap banned ho humare updates channel se. ❌")
            return False
        return True
    except UserNotParticipant:
        # Hinglish Interface Modification
        invite_link = f"https://t.me/{FORCE_SUB_CHANNEL}"
        await message.reply_text(
            text=f"**Oye {message.from_user.first_name}! रुको ज़रा... 👋**\n\n"
                 "Aapne abhi tak humara updates channel join nahi kiya hai. "
                 "Bot use karne ke liye pehle channel join karo, phir 'Try Again' button pe click karna!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Updates Channel 📢", url=invite_link)],
                [InlineKeyboardButton("Try Again 🔄", url=f"https://t.me/{client.username}?start={message.text.split()[1] if len(message.text.split()) > 1 else ''}")]
            ])
        )
        return False
    except Exception as e:
        # Agar koi aur error aaye toh bot ko rukne mat do
        return True

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time
