from swagger_server.dao.manager import Manager
from swagger_server.models_db.content_filter_db import ContentFilter


class ContentFilterManager(Manager):

    @staticmethod
    def create_content_filter(content_filter: ContentFilter):
        Manager.create(content_filter=content_filter)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.get(id_)

    def retrieve_by_user_id(user_id):
        Manager.check_none(user_id=user_id)
        return ContentFilter.query.filter_by(user_id=user_id).all()

    @staticmethod
    def retrieve_name(id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.filter(id=id_).name

    @staticmethod
    def retrieve_words(id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.filter(id=id_).words

    @staticmethod
    def retrieve_private(id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.filter(id=id_).private

    @staticmethod
    def update_content_filter_info(content_filter: ContentFilter):
        Manager.update(content_filter=content_filter)

    @staticmethod
    def delete_content_filter_info(content_filter: ContentFilter):
        Manager.delete(content_filter=content_filter)

    @staticmethod
    def delete_content_filter_by_id(id_: int):
        cf = ContentFilterManager.retrieve_by_id(id=id_)
        ContentFilterManager.delete_lottery_info(cf)
