from sqlalchemy import Column, String, Integer
from Azazel.core.SQL import BASE, SESSION

class BotLog(BASE):

    __tablename__ = "botlog_group_id"
    user_id = Column(String(14), primary_key=True)
    group_id = Column(Integer, nullable=False)

    def __init__(self, user_id, group_id):
        self.user_id = str(user_id)
        self.group_id = group_id

BotLog.__table__.create(checkfirst=True)

def get_botlog(user_id):
    try:
        botlog = SESSION.query(BotLog).get(str(user_id))
        return botlog.group_id if botlog else None
    finally:
        SESSION.close()

def set_botlog(user_id, group_id):
    botlog = SESSION.query(BotLog).get(str(user_id))
    if botlog:
        botlog.group_id = group_id
    else:
        botlog = BotLog(user_id, group_id)
        SESSION.add(botlog)
    SESSION.commit()
    SESSION.close()
