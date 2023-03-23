
import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from . import *


from Azazel.core.SQL import no_log_pms_sql
from Azazel.core.SQL.globals import addgvar, gvarstatus
from ubotlibs.ubot.utils.tools import get_arg



class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Client.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def monito_p_m_s(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    if not no_log_pms_sql.is_approved(message.chat.id) and message.chat.id != 777000:
        if LOG_CHATS_.RECENT_USER != message.chat.id:
            LOG_CHATS_.RECENT_USER = message.chat.id
            if LOG_CHATS_.NEWPM:
                await LOG_CHATS_.NEWPM.edit(
                    LOG_CHATS_.NEWPM.text.replace(
                        "💌 <b> PESAN BARU </b>",
                        f" • `{LOG_CHATS_.COUNT}` **Pesan**",
                    )
                )
                LOG_CHATS_.COUNT = 0
            LOG_CHATS_.NEWPM = await client.send_message(
                BOTLOG_CHATID,
                f"💌 <b> PESAN BARU </b>\n<b> • Dari :</b> {message.from_user.mention}\n<b> • User ID :</b> <code>{message.from_user.id}</code>",
                parse_mode=enums.ParseMode.HTML,
            )
        try:
            async for pmlog in client.search_messages(message.chat.id, limit=1):
                await pmlog.forward(BOTLOG_CHATID)
            LOG_CHATS_.COUNT += 1
        except BaseException:
            pass


@Client.on_message(filters.group & filters.mentioned & filters.incoming)
async def log_tagged_messages(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        return
    if (no_log_pms_sql.is_approved(message.chat.id)) or (BOTLOG_CHATID == -100):
        return
    result = f"<b>📨 Anda Telah Di Tag</b>\n<b> • Dari : </b>{message.from_user.mention}"
    result += f"\n<b> • Grup : </b>{message.chat.title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>Lihat Pesan</a>"
    result += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await client.send_message(
        BOTLOG_CHATID,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@Ubot(["pmlog"], "")
async def set_pmlog(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return await message.reply(
            "**Untuk Menggunakan Module ini, anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**"
        )
    tai = get_arg(message)
    if tai == "off":
        mati = False
    elif tai == "on":
        mati = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if mati:
            await message.edit("**PM LOG Sudah Diaktifkan**")
        else:
            addgvar("PMLOG", mati)
            await message.edit("**PM LOG Berhasil Dimatikan**")
    elif mati:
        addgvar("PMLOG", mati)
        await message.edit("**PM LOG Berhasil Diaktifkan**")
    else:
        await message.edit("**PM LOG Sudah Dimatikan**")


@Ubot(["taglog"], "")
async def set_gruplog(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return await message.edit(
            "**Untuk Menggunakan Module ini, anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**"
        )
    cot = get_arg(message)
    if cot == "off":
        noob = False
    elif cot == "on":
        noob = True
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if noob:
            await message.edit("**Group Log Sudah Diaktifkan**")
        else:
            addgvar("GRUPLOG", noob)
            await message.edit("**Group Log Berhasil Dimatikan**")
    elif noob:
        addgvar("GRUPLOG", noob)
        await message.edit("**Group Log Berhasil Diaktifkan**")
    else:
        await message.edit("**Group Log Sudah Dimatikan**")


add_command_help(
    "Logger",
    [
        [
            "pmlog [on atau off]",
            "Untuk mengaktifkan atau menonaktifkan log pesan pribadi yang akan di forward ke grup log.",
        ],
        [
            "taglog [on atau off]",
            "Untuk mengaktifkan atau menonaktifkan tag grup, yang akan masuk ke grup log.",
        ],
    ],
)
