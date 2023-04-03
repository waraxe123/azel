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


def load_blacklist_chat():
    with BLACKLIST_LOCK:
        monyet = SESSION.query(BlacklistChat).all()
        for chat in monyet:
            user_id = chat.user_id
            chat_id = chat.chat_id
            if CHAT_BLACKLISTS.get(user_id) is None:
                CHAT_BLACKLISTS[user_id] = {chat_id}
            else:
                CHAT_BLACKLISTS[user_id].add(chat_id)
            BLACKLIST_CHAT.add(chat_id)


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
        BLACKLIST_CHAT.add(chat_id)
        SESSION.close()
        return True

def rm_blchat(user_id, chat_id):
    with BLACKLIST_LOCK:
        bacot = SESSION.query(BlacklistChat).get((str(user_id), chat_id))
        if bacot:
            if chat_id in CHAT_BLACKLISTS.get(str(user_id), set()):
                CHAT_BLACKLISTS.get(str(user_id), set()).remove(chat_id)

            SESSION.delete(bacot)
            SESSION.commit()
            SESSION.close()
            return True


#        SESSION.close()
#        return True
load_blacklist_chat()