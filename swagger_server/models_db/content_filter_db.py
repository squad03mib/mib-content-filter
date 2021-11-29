from swagger_server import db


class ContentFilter(db.Model):

    __tablename__ = 'content_filter'

    SERIALIZE_LIST = ['id', 'name', 'words',
                      'private']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    words = db.Column(db.Unicode(128))
    private = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(ContentFilter, self).__init__(*args, **kw)

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_words(self, words):
        self.words = words

    def set_private(self, private):
        self.private = private

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
