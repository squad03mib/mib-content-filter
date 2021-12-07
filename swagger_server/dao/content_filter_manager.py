from swagger_server.dao.manager import Manager
from swagger_server.models.content_filter_info import ContentFilterInfo
from swagger_server.models_db.content_filter_db import ContentFilter, UserContentFilter
from swagger_server import db

class ContentFilterManager(Manager):

    @staticmethod
    def create_content_filter(content_filter: ContentFilter):
        Manager.create(content_filter=content_filter)
        return content_filter

    @staticmethod
    def retrieve_list_by_user_id(user_id):
        Manager.check_none(user_id=user_id)
        
        return db.session.query(ContentFilter, UserContentFilter)\
            .filter(UserContentFilter.filter_id_user==user_id)\
            .join(ContentFilter).filter(ContentFilter.filter_private.is_(True)).union_all(
                    db.session.query(ContentFilter,UserContentFilter)\
                        .filter(ContentFilter.filter_private.is_(False))\
                        .join(UserContentFilter, UserContentFilter.filter_id_user==user_id, isouter=True)).all()
                        
    def V2_get_filter_by_id(id_):
        Manager.check_none(id=id_)
        return db.session.query(ContentFilter).filter(ContentFilter.filter_id==id_).first()
    
    def V2_get_user_filter(filter_id, user_id):
        return db.session.query(UserContentFilter).filter(UserContentFilter.filter_id==filter_id,
            UserContentFilter.filter_id_user==user_id).first()
    
    def V2_set_user_filter_status(user_content_filter :UserContentFilter, active :bool):
        user_content_filter.filter_active = active
        Manager.update()
