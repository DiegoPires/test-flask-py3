#import zlib
#import json
#import re
import datetime
from app import dbNoSql as db

#ENCRYPTER = None


class Process(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def __repr__(self):
        return "<Process '%s'>" % self.name

    meta = {
        'indexes': ['-created_at', 'name'],
        'ordering': ['-created_at']
    }


class Window(db.Document):
    title = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    process = db.StringField(required=True)

    def __init__(self, title, process):
        self.title = title
        self.process = process

    def __repr__(self):
        return "<Window '%s'>" % (self.title)

    meta = {
        'indexes': ['-created_at', 'title'],
        'ordering': ['-created_at']
    }

'''
class Geometry(SpookMixin, Base):
    xpos = Column(Integer, nullable=False)
    ypos = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

    Index('idx_geo', 'xpos', 'ypos', 'width', 'height')

    def __init__(self, x, y, width, height):
        self.xpos = x
        self.ypos = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "<Geometry (%d, %d), (%d, %d)>" % (self.xpos, self.ypos, self.width, self.height)


class Click(SpookMixin, Base):
    button = Column(Integer, nullable=False)
    press = Column(Boolean, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    nrmoves = Column(Integer, nullable=False)

    process_id = Column(Integer, ForeignKey('process.id'), nullable=False, index=True)
    process = relationship("Process", backref=backref('clicks'))

    window_id = Column(Integer, ForeignKey('window.id'), nullable=False)
    window = relationship("Window", backref=backref('clicks'))

    geometry_id = Column(Integer, ForeignKey('geometry.id'), nullable=False)
    geometry = relationship("Geometry", backref=backref('clicks'))

    def __init__(self, button, press, x, y, nrmoves, process_id, window_id, geometry_id):
        self.button = button
        self.press = press
        self.x = x
        self.y = y
        self.nrmoves = nrmoves

        self.process_id = process_id
        self.window_id = window_id
        self.geometry_id = geometry_id

    def __repr__(self):
        return "<Click (%d, %d), (%d, %d, %d)>" % (self.x, self.y, self.button, self.press, self.nrmoves)


def pad(s, padnum):
    ls = len(s)
    if ls % padnum == 0:
        return s
    return s + '\0' * (padnum - (ls % padnum))


def maybe_encrypt(s, other_encrypter=None):
    if other_encrypter is not None:
        s = pad(s, 8)
        s = other_encrypter.encrypt(s)
    elif ENCRYPTER:
        s = pad(s, 8)
        s = ENCRYPTER.encrypt(s)
    return s


def maybe_decrypt(s, other_encrypter=None):
    if other_encrypter is not None:
        s = other_encrypter.decrypt(s)
    elif ENCRYPTER:
        s = ENCRYPTER.decrypt(s)
    return s


class Keys(SpookMixin, Base):
    text = Column(Binary, nullable=False)
    started = Column(DateTime, nullable=False)

    process_id = Column(Integer, ForeignKey('process.id'), nullable=False, index=True)
    process = relationship("Process", backref=backref('keys'))

    window_id = Column(Integer, ForeignKey('window.id'), nullable=False)
    window = relationship("Window", backref=backref('keys'))

    geometry_id = Column(Integer, ForeignKey('geometry.id'), nullable=False)
    geometry = relationship("Geometry", backref=backref('keys'))

    nrkeys = Column(Integer, index=True)

    keys = Column(Binary)
    timings = Column(Binary)

    def __init__(self, text, keys, timings, nrkeys, started, process_id, window_id, geometry_id):
        ztimings = zlib.compress(json.dumps(timings))

        self.encrypt_text(text)
        self.encrypt_keys(keys)

        self.nrkeys = nrkeys
        self.timings = ztimings
        self.started = started

        self.process_id = process_id
        self.window_id = window_id
        self.geometry_id = geometry_id

    def encrypt_text(self, text, other_encrypter=None):
        ztext = maybe_encrypt(text, other_encrypter=other_encrypter)
        self.text = ztext

    def encrypt_keys(self, keys, other_encrypter=None):
        zkeys = maybe_encrypt(zlib.compress(json.dumps(keys)),
                              other_encrypter=other_encrypter)
        self.keys = zkeys

    def decrypt_text(self):
        return maybe_decrypt(self.text)

    def decrypt_humanreadable(self):
        return self.to_humanreadable(self.decrypt_text())

    def decrypt_keys(self):
        keys = maybe_decrypt(self.keys)
        return json.loads(zlib.decompress(keys))

    def to_humanreadable(self, text):
        backrex = re.compile("\<\[Backspace\]x?(\d+)?\>",re.IGNORECASE)
        matches = backrex.search(text)
        while matches is not None:
            backspaces = matches.group(1)
            try:
                deletechars = int(backspaces)
            except TypeError:
                deletechars = 1

            newstart = matches.start() - deletechars
            if newstart < 0:
                newstart = 0

            text = (text[:newstart] + text[matches.end():])
            matches = backrex.search(text)
        return text

    def load_timings(self):
        return json.loads(zlib.decompress(self.timings))

    def __repr__(self):
        return "<Keys %s>" % self.nrkeys
'''