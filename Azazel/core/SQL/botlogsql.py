from sqlalchemy import Column, String, Integer
from . import BASE, SESSION

class BotLog(BASE):
    __tablename__ = "group_id"
    user_id = Column(String(14), primary_key=True)
    group_id = Column(Integer, nullable=False)

    def __init__(self, user_id, group_id):
        self.user_id = str(user_id)
        self.group_id = int(group_id)

BotLog.__table__.create(checkfirst=True)


def get_botlog(user_id):
    try:
        botlog = SESSION.query(BotLog).get(str(user_id))
        return botlog if botlog else None
    finally:
        SESSION.close()

def set_botlog(user_id, group_id):
    botlog = SESSION.query(BotLog).get(str(user_id))
    if botlog:
        botlog.group_id = int(group_id)
    else:
        botlog = BotLog(user_id=user_id, group_id=group_id)
        SESSION.add(botlog)
    SESSION.commit()
    SESSION.close()



async def get_log_grup():
    user = await bot.get_me()
    user_id = user.id
    user_data = SESSION.query(BotLogGroup).filter(BotLogGroup.user_id == user_id).first()
    return user_data.group_id if user_data else None

async def set_log_grup(group_id: int):
    user = await bot.get_me()
    user_id = user.id
    user_data = SESSION.query(BotLogGroup).filter(BotLogGroup.user_id == user_id).first()
    if user_data:
        user_data.group_id = group_id
    else:
        user_data = BotLogGroup(user_id=user_id, group_id=group_id)
        SESSION.add(user_data)
    SESSION.commit()
    SESSION.close()


async def buat_log(bot):
    user = await bot.get_me()
    user_id = user.id
    botlog_data = SESSION.query(BotLog).filter(BotLog.user_id == user_id).first()

    if botlog_data:
        botlog_chat_id = botlog_data.group_id
    else:
        group_name = 'Azazel Project Bot Log'
        group_description = 'Jangan Hapus Atau Keluar Dari Grup Ini\n\nCreated By @AzazelProjectBot.\nJika menemukan kendala atau ingin menanyakan sesuatu\nHubungi : @KynanSupport.'
        group = await bot.create_supergroup(group_name, group_description)
        botlog_chat_id = group.id
        text = 'Grup Log Berhasil Dibuat,\nKetik `id` untuk mendapatkan id log grup\nKemudian ketik `setlog` ID_GROUP\n\nContoh : setlog -100749492984'
        await bot.send_message(botlog_chat_id, text)

        botlog_data = BotLog(user_id=user_id, group_id=botlog_chat_id)
        SESSION.add(botlog_data)
        SESSION.commit()

    SESSION.close()
    return botlog_chat_id