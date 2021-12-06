from swagger_server.dao.manager import Manager
from swagger_server.models_db.content_filter_db import ContentFilter, UserContentFilter
from swagger_server import db

class ContentFilterManager(Manager):

    @staticmethod
    def create_content_filter(content_filter: ContentFilter):
        Manager.create(content_filter=content_filter)
        return content_filter

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return ContentFilter.query.filter(ContentFilter.filter_id == id_)

    @staticmethod
    def retrieve_by_id_and_user(user_id, id_):
        Manager.check_none(id=id_)
        return db.session.query(UserContentFilter,ContentFilter).filter(ContentFilter.filter_id == UserContentFilter.filter_id).filter(UserContentFilter.filter_id_user == user_id, UserContentFilter.filter_id == id_)

    @staticmethod
    def retrieve_list_by_user_id(user_id):
        Manager.check_none(user_id=user_id)
        return db.session.query(UserContentFilter,ContentFilter).filter(ContentFilter.filter_id == UserContentFilter.filter_id).filter(UserContentFilter.filter_id_user == user_id)

    def toggle_content_filter(user_id,id_):
        Manager.check_none(id=id_)
        content_filter = UserContentFilter.query.filter(UserContentFilter.filter_id == id_).filter(UserContentFilter.filter_id_user==user_id).first()
        if content_filter.filter_active is True:
            content_filter.filter_active = False
        else:
            content_filter.filter_active = True
        Manager.update()
        return content_filter
    
    def V2_get_filter_by_id(id_):
        Manager.check_none(id=id_)
        return db.session.query(ContentFilter).filter(ContentFilter.filter_id==id_).first()
    
    def V2_get_user_filter(filter_id, user_id):
        return db.session.query(UserContentFilter).filter(UserContentFilter.filter_id==filter_id,
            UserContentFilter.filter_id_user==user_id).first()
    
    def V2_set_user_filter_status(user_content_filter :UserContentFilter, active :bool):
        user_content_filter.filter_active = active
        Manager.update()
        return user_content_filter

'''
    @staticmethod
    def delete_content_filter_info(content_filter: ContentFilter):
        Manager.delete(content_filter=content_filter)

    @staticmethod
    def delete_content_filter_by_id(id_: int):
        cf = ContentFilterManager.retrieve_by_id(filter_id=id_)
        ContentFilterManager.delete_lottery_info(cf)
'''
