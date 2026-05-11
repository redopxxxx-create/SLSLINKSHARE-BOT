# +++ Modified By [telegram username: @Codeflix_Bots
import os
import re
from os import environ
import logging
from logging.handlers import RotatingFileHandler

# Pattern for chat id check (Original logic maintain karne ke liye)
id_pattern = re.compile(r'^.\d+$')

# Recommended
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN","7585379584:AAH9B9q6uwChcGZKP3B2XyswqHjvlCg7fUI")
APP_ID = int(os.environ.get("APP_ID","25436585"))
API_HASH = os.environ.get("API_HASH","294890dbd5c747557ee3205daaefc922")

# Main
OWNER_ID = int(os.environ.get("OWNER_ID", "7977515080")) # Yahan variable name fix kiya
PORT = os.environ.get("PORT", "8080")

# --- FORCE SUB SYSTEM ---
# Yahan apne channel ka username daalo bina @ ke (e.g. "Starlight_Animes")
FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "Starlight_Animes") 

# Database
DB_URI = os.environ.get("DB_URI", "mongodb+srv://itzsiddhant321_db_user:QaqPa4G1ovhRr6d3@cluster0.re1tk0z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "link")

#Auto approve 
CHAT_ID = [int(app_chat_id) if id_pattern.search(app_chat_id) else app_chat_id for app_chat_id in environ.get('CHAT_ID', '-1002903445682').split()] 
TEXT = environ.get("APPROVED_WELCOME_TEXT", "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n\‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Codeflix_Bots</b>")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

# Default
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start pic
START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg")

# --- HINGLISH UI IMPROVED MESSAGES ---
START_MSG = os.environ.get("START_MESSAGE", "<b>Hey {mention}! 👋\n\nMain ek advanced Link Sharing Bot hoon. Mere saath aap apne links secure rakh sakte ho copyright issues se.\n\nBas koi bhi file forward karo aur magic dekho! ✨\n\n<blockquote>‣ Maintained by : <a href='https://t.me/codeflix_bots'>Yato</a></blockquote></b>")

HELP = os.environ.get("HELP_MESSAGE", "<b><blockquote expandable>Kaise use karein?\n\n1. Bot ko apne channel mein admin banao.\n2. Koi bhi file yahan forward karo.\n3. Bot aapko ek secure link de dega.\n\nDeveloper: <a href='https://t.me/proyato'>Yato</a></blockquote></b>")

ABOUT = os.environ.get("ABOUT_MESSAGE", "<b><blockquote expandable>Ye bot Yato (@ProYato) ne banaya hai taaki aapke channels copyright se bache rahein. Ismein high-speed storage aur force sub system integrated hai.</b>")

ABOUT_TXT = """<b>›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/otakuflix_network'>ᴏᴛᴀᴋᴜғʟɪx</a>
<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/codeflix_bots'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>
›› ᴏᴡɴᴇʀ: <a href='https://t.me/cosmic_freak'>ʏᴀᴛᴏ</a>
›› ʟᴀɴɢᴜᴀɢᴇ: Pʏᴛʜᴏɴ 3
›› ʟɪʙʀᴀʀʏ: Pʏʀᴏɢʀᴀᴍ ᴠ2
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ProYato</b></blockquote>""" 

CHANNELS_TXT = """<b>›› ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/anime_nation_hindii'>ᴀɴɪᴍᴇ ᴄʀᴜɪsᴇ</a>
<blockquote expandable>›› ᴍᴏᴠɪᴇs: <a href='https://t.me/AniPulse_Hindi'>ᴍᴏᴠɪᴇғʟɪx sᴘᴏᴛ</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ItsRyoSudhish</b></blockquote>"""

# Default
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "⚠️ Sorry bro, aap mere master nahi ho! 🙃"

# Logging
LOG_FILE_NAME = "links-sharingbot.txt"
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "-1002903445682")) 

try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "7738104912 7977515080").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

ADMINS.append(OWNER_ID)
ADMINS.append(6497757690)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
