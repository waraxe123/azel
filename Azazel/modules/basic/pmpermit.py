
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from sqlalchemy.exc import IntegrityError

from . import *
from Azazel import TEMP_SETTINGS
from Azazel.core.SQL.botlogsql import *
from Azazel.core.SQL.globals import *
from ubotlibs.ubot.utils.tools import get_arg

PMPERMIT = False

DEF_UNAPPROVED_MSG = (
"╔═════════════════════╗\n"
"ㅤ   ⚡️ ᴡᴇʟᴄᴏᴍᴇ  ᴇᴠᴇʀʏʙᴏᴅʏ ⚡️\n"
"╚═════════════════════╝\n"
"➣ ᴊᴀɴɢᴀɴ  sᴘᴀᴍ  ᴄʜᴀᴛ  ᴛᴜᴀɴ  sᴀʏᴀ\n"
"➣ ᴀᴛᴀᴜ ᴀɴᴅᴀ ᴏᴛᴏᴍᴀᴛɪs  sᴀʏᴀ ʙʟᴏᴋɪʀ\n"
"╔═════════════════════╗\n"
"  ㅤ     ⚡𝕡𝕖𝕤𝕒𝕟  𝕠𝕥𝕠𝕞𝕒𝕥𝕚𝕤⚡\n"
"     ㅤ  ✮𝙰𝚉𝙰𝚉𝙴𝙻 𝙿𝚁𝙾𝙹𝙴𝙲𝚃✮ㅤㅤ  \n"
"╚═════════════════════╝"
)


@Client.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def incomingpm(client: Client, message: Message):
    try:
        from Azazel.core.SQL.globals import gvarstatus
        from Azazel.core.SQL.pm_permit_sql import is_approved
    except BaseException:
        pass
      
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return
    if await auto_accept(client, message) or message.from_user.is_self:
        message.continue_propagation()
    if message.chat.id != 777000:
        PM_LIMIT = gvarstatus(str(user_id), "PM_LIMIT") or 5
        getmsg = gvarstatus(str(user_id), "unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

        apprv = is_approved(message.chat.id)
        if not apprv and message.text != UNAPPROVED_MSG:
            if message.chat.id in TEMP_SETTINGS["PM_LAST_MSG"]:
                prevmsg = TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                if message.text != prevmsg:
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=5,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    if TEMP_SETTINGS["PM_COUNT"][message.chat.id] < (int(PM_LIMIT) - 1):
                        ret = await message.reply_text(UNAPPROVED_MSG)
                        TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            else:
                ret = await message.reply_text(UNAPPROVED_MSG)
                if ret.text:
                    TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            if message.chat.id not in TEMP_SETTINGS["PM_COUNT"]:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = 1
            else:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = (
                    TEMP_SETTINGS["PM_COUNT"][message.chat.id] + 1
                )
            if TEMP_SETTINGS["PM_COUNT"][message.chat.id] > (int(PM_LIMIT) - 1):
                await message.reply("**Maaf anda Telah Di Blokir Karna Spam Chat**")
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                await client.block_user(message.chat.id)

    message.continue_propagation()


async def auto_accept(client, message):
    try:
        from Azazel.core.SQL.pm_permit_sql import approve, is_approved
    except BaseException:
        pass

    if message.chat.id in DEVS:
        try:
            approve(message.chat.id)
            await client.send_message(
                message.chat.id,
                f"<b>Menerima Pesan!!!</b>\n{message.from_user.mention} <b>Terdeteksi Developer Azazel-Project</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except IntegrityError:
            pass
    if message.chat.id not in [client.me.id, 777000]:
        if is_approved(message.chat.id):
            return True

        async for msg in client.get_chat_history(message.chat.id, limit=1):
            if msg.from_user.id == client.me.id:
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                try:
                    approve(chat.id)
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=5,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    return True
                except BaseException:
                    pass

    return False


@Ubot(["ok", "y"], "")
async def approvepm(client, message):
    try:
        from Azazel.core.SQL.pm_permit_sql import approve
    except BaseException:
        await message.edit("Running on Non-SQL mode!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("Anda tidak dapat menyetujui diri sendiri.")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit(
                "Saat ini Anda tidak sedang dalam PM dan Anda belum membalas pesan seseorang."
            )
            return
        name0 = aname.first_name
        uid = aname.id

    try:
        approve(uid)
        await message.edit(f"**Menerima Pesan Dari** [{name0}](tg://user?id={uid})!")
    except IntegrityError:
        await message.edit(
            f"[{name0}](tg://user?id={uid}) mungkin sudah disetujui untuk PM."
        )
        return


@Ubot(["no", "g"], "")
async def disapprovepm(client, message):
    try:
        from Azazel.core.SQL.pm_permit_sql import dissprove
    except BaseException:
        await message.edit("Running on Non-SQL mode!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("Anda tidak bisa menolak diri sendiri.")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit(
                "Saat ini Anda tidak sedang dalam PM dan Anda belum membalas pesan seseorang."
            )
            return
        name0 = aname.first_name
        uid = aname.id

    dissprove(uid)

    await message.edit(
        f"**Pesan** [{name0}](tg://user?id={uid}) **Telah Ditolak, Mohon Jangan Melakukan Spam Chat!**"
    )


@Ubot(["setlimit"], "")
async def setpm_limit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.edit(
            f"**Anda Harus Menyetel Var** `PM_AUTO_BAN` **Ke** `True`\n\n**Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `{cmd}setvar PM_AUTO_BAN True`"
        )
    try:
        from Azazel.core.SQL.globals import addgvar
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    input_str = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not input_str:
        return await message.edit("**Harap masukan angka untuk PM_LIMIT.**")
    biji = await message.reply("`Processing...`")
    if input_str and not input_str.isnumeric():
        return await biji.edit("**Harap masukan angka untuk PM_LIMIT.**")
    addgvar(str(user_id), "PM_LIMIT", input_str)
    await biji.edit(f"**Set PM limit to** `{input_str}`")


@Ubot(["antipm"], "")
async def onoff_pmpermit(client, message):
    user_id = client.me.id
    blok = get_arg(message)
    tai = False
    if blok == "off":
        tai = False
    elif blok == "on":
        tai = True
    elif tai:
        addgvar(str(user_id), "PMPERMIT", tai)
        await message.edit("**Antipm Berhasil Diaktifkan**")
    elif tai:
        delgvar(str(user_id), "PMPERMIT")
        await message.edit("**Antipm Berhasil Dimatikan**")
    else:
        await message.edit("**Antipm Sudah Dimatikan**")



@Ubot(["setpm"], "")
async def setpmpermit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.reply(
            "**Anda Harus Menyetel Var** `PM_AUTO_BAN` **Ke** `True`\n\n**Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import Azazel.core.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    tai = await message.reply("`Processing...`")
    nob = sql.gvarstatus(str(user_id), "unapproved_msg")
    message = message.reply_to_message
    if nob is not None:
        sql.delgvar(str(user_id), "unapproved_msg")
    if not message:
        return await tai.edit("**Mohon Reply Ke Pesan**")
    msg = message.text
    sql.addgvar(str(user_id), "unapproved_msg", msg)
    
    await tai.edit("**Pesan Berhasil Disimpan**")


@Ubot(["getpm"], "")
async def get_pmermit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.edit(
            "**Anda Harus Menyetel Var** `PM_AUTO_BAN` **Ke** `True`\n\n**Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import Azazel.core.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    zel = await message.reply("`Processing...`")
    nob = sql.gvarstatus(str(user_id), "unapproved_msg")
    if nob is not None:
        await zel.edit("**Pesan PMPERMIT Yang Sekarang:**" f"\n\n{nob}")
    else:
        
        await zel.edit(
            "**Anda Belum Menyetel Pesan Costum PMPERMIT,**\n"
            f"**Masih Menggunakan Pesan PM Default:**\n\n{DEF_UNAPPROVED_MSG}"
        )


@Ubot(["resetpm"], "")
async def reset_pmpermit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.edit(
            f"**Anda Harus Menyetel Var** `PM_AUTO_BAN` **Ke** `True`\n\n**Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `{cmd}setvar PM_AUTO_BAN True`"
        )
    try:
        import Azazel.core.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    sok = await message.reply("`Processing...`")
    nob = sql.gvarstatus(str(user_id), "unapproved_msg")

    if nob is None:
        await sok.edit("**Pesan Antipm Anda Sudah Default**")
    else:
        sql.delgvar(str(user_id), "unapproved_msg")
        
        await sok.edit("**Berhasil Mengubah Pesan Custom Antipm menjadi Default**")


add_command_help(
    "PMPermit",
    [
        [
            f"ok atau y",
            "Menerima pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm",
        ],
        [
            f"no atau g",
            "Menolak pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm",
        ],
        [
            "pmlimit <angka>",
            "Untuk mengcustom pesan limit auto block pesan",
        ],
        [
            "setpm <balas ke pesan>",
            "Untuk mengcustom pesan PMPERMIT untuk orang yang pesannya belum diterima.",
        ],
        [
            "getpm",
            "Untuk melihat pesan PMPERMIT.",
        ],
        [
            "resetpm",
            "Untuk Mereset Pesan PMPERMIT menjadi DEFAULT",
        ],
        [
            "antipm [on/off]",
            "Untuk mengaktifkan atau menonaktifkan PMPERMIT",
        ],
    ],
)
