from swagger_server import db


class ContentFilter(db.Model):

    __tablename__ = 'content_filter'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    words = db.Column(db.Unicode(128))
    private = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(ContentFilter, self).__init__(*args, **kw)


class UserContentFilter(db.Model):

    __tablename__ = 'user_content_filter'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, ForeignKey('user.id'))
    id_content_filter = db.Column(db.Integer, ForeignKey('content_filter.id'))
    active = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(UserContentFilter, self).__init__(*args, **kw)
