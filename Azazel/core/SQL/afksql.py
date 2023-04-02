from sqlalchemy import Boolean, Column, String, UnicodeText

from . import BASE, SESSION

Owner = 0


class AFK(BASE):
    __tablename__ = "afk"
    user_id = Column(String(14), primary_key=True)
    is_afk = Column(Boolean, default=False)
    reason = Column(UnicodeText, default=False)
    def __init__(self, user_id, is_afk, reason):
        self.user_id = str(user_id)
        self.is_afk = is_afk
        self.reason = reason
    def __repr__(self):
        return "<AFK {}>".format(self.user_id)


AFK.__table__.create(checkfirst=True)
SEMPAK = {}


def set_afk(user_id, afk, reason):
    global MY_AFK
    afk_db = SESSION.query(AFK).get(str(user_id))
    if afk_db:
        SESSION.delete(afk_db)
    afk_db = AFK(str(user_id), afk, reason)
    SESSION.add(afk_db)
    SESSION.commit()
    SEMPAK[str(user_id)] = {"afk": afk, "reason": reason}


def get_afk(user_id):
    return SEMPAK.get(str(user_id))


def __load_afk():
    global SEMPAK
    try:
        SEMPAK = {}
        qall = SESSION.query(AFK).all()
        for x in qall:
            SEMPAK[int(x.user_id)] = {"afk": x.is_afk, "reason": x.reason}
    finally:
        SESSION.close()


__load_afk()
