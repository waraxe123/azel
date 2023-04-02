"""
from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import Message
from Azazel.core.SQL.afksql import *
from Azazel.core.SQL.botlogsql import *
from ubotlibs.ubot.utils import get_text
from . import *


@Ubot("afk", "")
async def set_afk(client, message):
    if len(message.command) == 1:
        return await message.reply(f"**Gunakan format dengan berikan alasan**\n\n**Contoh** : `afk berak`")
    user_id = client.me.id
    botlog = get_botlog(str(user_id))
    ajg = await message.edit("Processing..")
    msge = None
    msge = get_text(message)
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if msge:
        msg = f"**❏ Sedang AFK**.\n** ╰ Alasan** : `{msge}`"
        await client.send_message(botlog, afkstr.format(msge))
        set_afk(user_id, afk_start, msge)
    else:
        msg = "**❏ Sedang AFK**."
        await client.send_message(botlog, afkstr.format(msge))
        set_afk(user_id, afk_start)
    await ajg.edit(msg)

@Client.on_message(
    is_afk
    & (filters.mentioned | filters.private)
    & ~filters.me
    & ~filters.bot
    & filters.incoming
)
async def afk_er(client, message):
    user_id = client.me.id
    if not message:
        return
    if not message.from_user:
        return
    if message.from_user.id == user_id:
        return
    use_r = int(user_id)
    if use_r not in afk_sanity_check.keys():
        afk_sanity_check[use_r] = 1
    else:
        afk_sanity_check[use_r] += 1
    if afk_sanity_check[use_r] == 5:
        await message.reply_text(
            "**❏ Sedang AFK**."
        )
        afk_sanity_check[use_r] += 1
        return
    if afk_sanity_check[use_r] > 5:
        return
    bsgt = check_afk_status(user_id)
    reason = bsgt["reason"]
    if reason == "":
        reason = None
    back_alivee = datetime.now()
    afk_start = bsgt["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    message_to_reply = (
        f"**❏ Sedang AFK**\n** ├ Waktu** :`{total_afk_time}`\n** ╰ Alasan** : `{reason}`"
        if reason
        else f"**❏ Sedang AFK**\n** ╰ Waktu** :`{total_afk_time}`"
    )
    await message.reply(message_to_reply)
    

@Client.on_message(filters.outgoing & filters.me & is_afk)
async def no_afke(client, message):
    user_id = client.me.id
    botlog = get_botlog(str(user_id))
    nyet = check_afk_status(user_id)
    back_alivee = datetime.now()
    afk_start = nyet["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    kk = await message.reply(f"**❏ Saya Kembali.**\n** ╰ AFK Selama** : {total_afk_time}")
    await kk.delete()
    rm_afk(user_id)
    await client.send_message(botlog, onlinestr.format(total_afk_time))

add_command_help(
    "Afk",
    [
        [f"afk","Mengaktifkan mode afk.",
        ],
    ],
)
"""