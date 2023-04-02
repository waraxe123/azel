"""

import threading
from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import Message
from . import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText, String


class AFK(BASE):
    __tablename__ = "afk"

    user_id = Column(String(14), primary_key=True)
    is_afk = Column(Boolean)
    time = Column(String)
    reason = Column(UnicodeText)

    def __init__(self, user_id, time="", reason="", is_afk=True):
        self.user_id = str(user_id)
        self.time = time
        self.reason = reason
        self.is_afk = is_afk

    def __repr__(self):
        return "afk_status for {}".format(self.user_id)



AFK.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

AFK_USERS = {}

"""
def is_afk(user_id):
    return user_id in AFK_USERS
"""

afk_sanity_check: dict = {}
afkstr = """
#AFK Hidup\n alasan {}
"""
onlinestr ="""
#AFK Mati\nAfk dari {}
"""
async def is_afk_(f, client, message):
    user_id = client.me.id
    af_k_c = check_afk_status(user_id)
    if af_k_c:
        return bool(True)
    else:
        return bool(False)
    
is_afk = filters.create(func=is_afk_, name="is_afk_")

def check_afk_status(user_id):
    try:
        return SESSION.query(AFK).get(str(user_id))
    finally:
        SESSION.close()


def set_afk(user_id, time="", reason=""):
    with INSERTION_LOCK:
        tai = SESSION.query(AFK).get(str(user_id))
        if not tai:
            tai = AFK(str(user_id), time, reason, True)
        else:
            tai.is_afk = True
            tai.time = time
        AFK_USERS[str(user_id)] = time, reason
        SESSION.add(tai)
        SESSION.commit()


def rm_afk(user_id):
    with INSERTION_LOCK:
        ajg = SESSION.query(AFK).get(str(user_id))
        if ajg:
            if user_id in AFK_USERS:
                del AFK_USERS[str(user_id)]

            SESSION.delete(ajg)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def toggle_afk(user_id, time="", reason=""):
    with INSERTION_LOCK:
        bacot = SESSION.query(AFK).get(str(user_id))
        if not bacot:
            bacot = AFK(str(user_id), time, reason, True)
        elif bacot.is_afk:
            bacot.is_afk = False
        elif not bacot.is_afk:
            bacot.is_afk = True
            bacot.time = time
        SESSION.add(bacot)
        SESSION.commit()


def __load_afk_users():
    global AFK_USERS
    try:
        bangsat = SESSION.query(AFK).all()
        AFK_USERS = {user.user_id: user.time, user.reason for user in bangsat if user.is_afk}
    finally:
        SESSION.close()


__load_afk_users()
"""