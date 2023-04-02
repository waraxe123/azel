from sqlalchemy import Column, String, Integer, BigInteger
from . import BASE, SESSION
import threading

class BlacklistChat(BASE):
    __tablename__ = "blacklistchat"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(BigInteger, nullable=False)

    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = int(chat_id)

BlacklistChat.__table__.create(checkfirst=True)

BLACKLIST_LOCK = threading.RLock()
BLACKLIST_CHAT = set()
CHAT_BLACKLISTS = {}


def get_blchat(user_id):
    return CHAT_BLACKLISTS.get(str(user_id), set())


def add_blchat(user_id, chat_id):
    with BLACKLIST_LOCK:
        kambing = BlacklistChat(str(user_id), chat_id)

        SESSION.merge(kambing)
        SESSION.commit()
        global CHAT_BLACKLISTS
        if CHAT_BLACKLISTS.get(str(user_id), set()) == set():
            CHAT_BLACKLISTS[str(user_id)] = {chat_id}
        else:
            CHAT_BLACKLISTS.get(str(user_id), set()).add(chat_id)


"""
def get_blchat(user_id):
    try:
        return SESSION.query(BlacklistChat).filter(BlacklistChat.user_id == str(user_id)).all()
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


def add_blchat(user_id, chat_id):
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
"""