from swagger_server import db
from sqlalchemy import ForeignKey, event
import json

class ContentFilter(db.Model):

    __tablename__ = 'content_filter'

    SERIALIZE_LIST = ['filter_id', 'filter_name', 'filter_words',
                      'filter_private']

    filter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filter_name = db.Column(db.Unicode(128))
    filter_words = db.Column(db.Text)
    filter_private = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(ContentFilter, self).__init__(*args, **kw)

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])


class UserContentFilter(db.Model):

    __tablename__ = 'user_content_filter'

    SERIALIZE_LIST = ['filter_id', 'filter_id_user', 'filter_id_key',
                      'filter_active']

    filter_id_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filter_id_user = db.Column(db.Integer)
    filter_id = db.Column(
        db.Integer, ForeignKey('content_filter.filter_id'))
    filter_active = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(UserContentFilter, self).__init__(*args, **kw)

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
