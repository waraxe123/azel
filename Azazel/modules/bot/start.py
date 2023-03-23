
import heroku3
import time
import re
import asyncio
import math
import shutil
import sys
import dotenv
import datetime
from dotenv import load_dotenv
from os import environ, execle, path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Azazel import *
from itertools import count
from Azazel.modules.basic import *

from pyrogram import *
from platform import python_version as py
from pyrogram import __version__ as pyro
from pyrogram.types import * 
from io import BytesIO

from Azazel.logging import LOGGER
from config import *

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Azazel"])

HAPP = None

load_dotenv()

session_counter = count(1)

ANU = """
❏ **Users** Ke {}
├╼ **Nama**: {}
╰╼ **ID**: {}
"""



@app.on_message(filters.command(["start"]))
async def start_(client: Client, message: Message):
    ADMIN1 = ADMIN1_ID[0]
    ADMIN2 = ADMIN2_ID[0]
    await message.reply_text(
        f"""<b>👋 Halo {message.from_user.first_name} \n
💭 Apa ada yang bisa saya bantu
💡 Jika ingin membuat bot premium . Kamu bisa hubungin admin dibawah ini membuat bot.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👮‍♂ Admin 1", url=f"https://t.me/kenapanan"),
                    InlineKeyboardButton(text="👮‍♂ Admin 2", url=f"https://t.me/bangjhorr"),
                ],
                  [
                     InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                  ],
             ]
        ),
     disable_web_page_preview=True
    )
    
        
@app.on_message(filters.private & filters.command("restart") & ~filters.via_bot
)
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply(" `Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("✅ **Bot has restarted !**\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Azazel"]
        execle(sys.executable, *args, environ)


@Client.on_message(filters.command("restart", "") & filters.me)
async def restart_bot(_, message: Message):
    try:
        await message.edit(" `Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await message.edit("✅ **Bot has restarted**\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Azazel"]
        execle(sys.executable, *args, environ)
        
