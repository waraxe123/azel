from sqlalchemy import Column, String, Integer, BigInteger
from . import BASE, SESSION

class BlacklistChat(BASE):
    __tablename__ = "blacklistchat"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(BigInteger, nullable=False)

    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = int(chat_id)

BlacklistChat.__table__.create(checkfirst=True)


def blacklisted_chats(user_id):
    try:
        return SESSION.query(BlacklistChat).get(str(user_id))
    finally:
        SESSION.close()

        
def get_blchat(user_id):
    try:
        return SESSION.query(BlacklistChat).get((str(user_id))
    finally:
        SESSION.close()


def rm_blchat(user_id, chat_id):
    sempak = get_blchat(user_id)
    if not sempak:
        return False
    rem = SESSION.query(BlacklistChat).get((str(user_id), chat_id))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def add_blacklist(user_id, chat_id):
    tai = get_blchat(user_id)
    if not tai:
        adder = BlacklistChat(str(user_id), chat_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(BlacklistChat).get((str(user_id), chat_id))
    SESSION.delete(rem)
    SESSION.commit()
    adder = BlacklistChat(str(user_id), chat_id)
    SESSION.add(adder)
    SESSION.commit()
    return False
