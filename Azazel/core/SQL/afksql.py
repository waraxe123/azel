import threading

from . import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText


class AFK(BASE):
    __tablename__ = "afk"

    user_id = Column(String(14), primary_key=True)
    is_afk = Column(Boolean)
    reason = Column(UnicodeText)

    def __init__(self, user_id, reason="", is_afk=True):
        self.user_id = str(user_id)
        self.reason = reason
        self.is_afk = is_afk

    def __repr__(self):
        return "afk_status for {}".format(self.user_id)


AFK.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

AFK_USERS = {}


def is_afk(user_id):
    return user_id in AFK_USERS


def check_afk_status(user_id):
    try:
        return SESSION.query(AFK).get(str(user_id))
    finally:
        SESSION.close()


def set_afk(user_id, reason=""):
    with INSERTION_LOCK:
        tai = SESSION.query(AFK).get(str(user_id))
        if not tai:
            tai = AFK(str(user_id), reason, True)
        else:
            tai.is_afk = True

        AFK_USERS[str(user_id)] = reason

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


def toggle_afk(user_id, reason=""):
    with INSERTION_LOCK:
        bacot = SESSION.query(AFK).get(str(user_id))
        if not bacot:
            bacot = AFK(str(user_id), reason, True)
        elif bacot.is_afk:
            bacot.is_afk = False
        elif not bacot.is_afk:
            bacot.is_afk = True
        SESSION.add(bacot)
        SESSION.commit()


def __load_afk_users():
    global AFK_USERS
    try:
        bangsat = SESSION.query(AFK).all()
        AFK_USERS = {user.user_id: user.reason for user in bangsat if user.is_afk}
    finally:
        SESSION.close()


__load_afk_users()
