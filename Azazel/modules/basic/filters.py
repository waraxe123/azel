

import re
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton as Ikb
from . import *
from Azazel.core.SQL.filtersql  import *
from Azazel.core import *


@Ubot("adfil", "")
async def save_filters(client, message):
    user_id = client.me.id
    chat_id = message.chat.id
    if len(message.command) < 2 or not message.reply_to_message:
        return await message.reply_text(
            f"**Gunakan Format:**\nbalas kepesan atau sticker `savefilter` [nama filter] untuk save filter."
        )
    if (
        not message.reply_to_message.text
        and not message.reply_to_message.sticker
    ):
        return await message.reply_text(
            "**Hanya bisa save text atau sticker.**"
        )
    keyword = message.text.split(None, 1)[1].strip()
    if not keyword:
        return await message.reply_text(
            f"**Gunakan Format:**\n`filter` [nama filter]"
        )
    
    if message.chat.id in BL_GCAST:
        await message.edit("Filter tidak diperkenankan di group support")
        return
    _type = "text" if message.reply_to_message.text else "sticker"
    reply = {
        "type": _type,
        "data": message.reply_to_message.text.markdown
        if _type == "text"
        else message.reply_to_message.sticker.file_id,
    }
    add_filter(str(user_id), str(chat_id), keyword, reply)
    await message.reply_text(f"**Filter {keyword} disimpan!.**")


@Ubot("filters", "") #lu gay
async def get_filterss(client, message):
    user_id = client.me.id
    chat_id = message.chat.id
    sempak = get_filters(str(user_id), str(chat_id))
    if not sempak:
        return await message.reply_text("**Tidak ada filter tersimpan di group ini.**")
    sempak.sort()
    msg = f"Daftar filter tersimpan di {message.chat.title}\n"
    for sempak in sempak:
        msg += f"**-** `{sempak}`\n"
    await message.reply_text(msg)

@Ubot("stfil", "") #lu gay
async def del_filter(client, message):
	  user_id = client.me.id
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply_text(f"**Gunakan Format:**\n`stopfilter` [nama filter]")
    keyword = message.text.split(None, 1)[1].strip()
    if not keyword:
        return await message.reply_text(f"**Gunakan format:**\n`stopfilter` [nama filter]")
    
    bajingan = remove_filter(str(user_id), str(chat_id), keyword)
    if bajingan:
        await message.reply_text(f"*Filter {keyword} berhasil dihapus.**")
    else:
        await message.reply_text("**Filter tidak ditemukan.**")

@Client.on_message(filters.text & ~filters.private & ~filters.via_bot & ~filters.forwarded,group=chat_filters_group)
async def filters_re(client, message):
    text = message.text.lower().strip()
    if not text:
        return
    user_id = client.me.id
    chat_id = message.chat.id
    babi = get_filters(str(user_id), str(chat_id))
    for word in babi:
        pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            sempak = get_filter(str(user_id), str(chat_id), word)
            data_type = sempak["type"]
            data = sempak["data"]
            if data_type == "text":
                keyb = None
                if re.findall(r"\[.+\,.+\]", data):
                    keyboard = extract_text_and_keyb(ikb, data)
                    if keyboard:
                        data, keyb = keyboard

                if message.reply_to_message:
                    await message.reply_to_message.reply_text(
                        data,
                        reply_markup=keyb,
                        disable_web_page_preview=True,
                    )

                    if text.startswith("~"):
                        await message.delete()
                    return

                return await message.reply_text(
                    data,
                    reply_markup=keyb,
                    disable_web_page_preview=True,
                )
            if message.reply_to_message:
                await message.reply_to_message.reply_sticker(data)

                if text.startswith("~"):
                    await message.delete()
                return
            return await message.reply_sticker(data)
        
add_command_help(
    "Filters",
    [
        [f"adfil <balas ke pesan atau sticker> <triger/nama filer>", "Save filters."],
        [f"stfil <triger/nama filter>", "Menghapus filter."],
        [f"filters", "Melihat list filter."],
    ],
)
