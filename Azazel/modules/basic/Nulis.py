from pyrogram import Client, filters
from pyrogram.types import Message
from . import *
import requests

@Ubot("nulis", "")
async def handwrite(client, message):
    if message.reply_to_message:
        monyet = message.reply_to_message.text
    else:
        monyet = message.text.split(None, 1)[1]
    babi = await message.reply("`Processing...`")
    ajg = requests.get(f"https://api.sdbots.tk/write?text={monyet}").url
    await message.reply_photo(
        photo=ajg,
        caption=f"**Ditulis Oleh :** {client.me.mention}")
    await babi.delete()


add_command_help(
    "Nulis",
    [
        [f"nulis [berikan pesan/balas ke pesan]", "Membuat Tulisan Untuk Kamu Yang Malas Nulis."],
    ],
)
