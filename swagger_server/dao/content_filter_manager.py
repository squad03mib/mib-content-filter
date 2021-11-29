from swagger_server.dao.manager import Manager
from swagger_server.models_db.content_filter_db import ContentFilter, UserContentFilter


class ContentFilterManager(Manager):

    @staticmethod
    def create_content_filter(content_filter: ContentFilter):
        Manager.create(content_filter=content_filter)
        return content_filter

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.get(id_)

    @staticmethod
    def retrieve_by_id_and_user(user_id, id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.join(UserContentFilter, ContentFilter.filter_id == UserContentFilter.filter_id).filter(UserContentFilter.filter_id_user == user_id, UserContentFilter.filter_id == id_)

    @staticmethod
    def retrieve_list_by_user_id(user_id):
        Manager.check_none(user_id=user_id)
        return ContentFilter.query.join(UserContentFilter, ContentFilter.filter_id == UserContentFilter.filter_id).filter(UserContentFilter.filter_id_user == user_id)

    def toggle_content_filter(id_, active):
        Manager.check_none(id=id_)
        content_filter = ContentFilter.query.get(id_)
        content_filter.active = active
        Manager.update()
        return content_filter

    @staticmethod
    def update_content_filter_info():
        Manager.update()

    @staticmethod
    def delete_content_filter_info(content_filter: ContentFilter):
        Manager.delete(content_filter=content_filter)

    @staticmethod
    def delete_content_filter_by_id(id_: int):
        cf = ContentFilterManager.retrieve_by_id(filter_id=id_)
        ContentFilterManager.delete_lottery_info(cf)
