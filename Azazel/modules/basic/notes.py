from asyncio import sleep
from pyrogram import Client, filters
from Azazel.core.SQL.notesql import *
from Azazel.core.SQL.botlogqsl import *
from pyrogram.types import Message
from ubotlibs.ubot.utils.tools import *
from . import *





@Ubot(["save"], "")
async def simpan_note(client, message):
    keyword = get_arg(message)
    user_id = message.from_user.id
    msg = message.reply_to_message
    botlog_chat_id = get_botlog(user_id)
    if not msg:
        return await message.reply("Tolong balas ke pesan")
    anu = await msg.forward(botlog_chat_id)
    msg_id = anu.id
    await client.send_message(botlog_chat_id,
        f"#NOTE\nKEYWORD: {keyword}"
        "\n\nPesan berikut disimpan sebagai data balasan catatan untuk obrolan, mohon JANGAN dihapus !!",
    )
    await sleep(1)
    add_note(str(user_id), keyword, msg_id)
    await message.reply(f"Berhasil menyimpan note {keyword}")


@Ubot(["get"], "")
async def panggil_notes(client, message):
    notename = get_arg(message)
    user_id = message.from_user.id
    note = get_note(str(user_id), notename)
    botlog_chat_id = await get_botlog(str(user_id))
    if not note:
        return await message.reply("Tidak ada catatan seperti itu.")
    msg_o = await client.get_messages(botlog_chat_id, int(note.f_mesg_id))
    await msg_o.copy(message.chat.id, reply_to_message_id=message.id)


@Ubot(["rm"], "")
async def remove_notes(client, message):
    notename = get_arg(message)
    user_id = message.from_user.id
    if rm_note(str(user_id), notename) is False:
        return await message.reply(
            "Tidak dapat menemukan catatan: {}".format(notename)
        )
    return await message.reply("Berhasil Menghapus Catatan: {}".format(notename))


@Ubot(["notes"], "")
async def list_notes(client, message):
    user_id = message.from_user.id
    notes = get_notes(str(user_id))
    if not notes:
        return await message.reply("Tidak ada catatan.")
    msg = f"**Daftar Catatan**\n\n"
    for note in notes:
        msg += f"• {note.keyword}\n"
    await message.reply(msg)


add_command_help(
    "Notes",
    [
        [f" save [text/reply]",
            "Simpan pesan ke Group. (bisa menggunakan stiker)"],
        [f" get [nama]",
            "Ambil catatan ke tersimpan"],
        [f" notes",
            "Lihat Daftar Catatan"],
        [f" rm [nama]",
            "Menghapus nama catatan"],
    ],
)
