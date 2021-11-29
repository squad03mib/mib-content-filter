import connexion
import six
from flask import jsonify

from swagger_server.models.content_filter import ContentFilter  # noqa: E501
from swagger_server.models.content_filter_info import ContentFilterInfo  # noqa: E501
from swagger_server.dao.content_filter_manager import ContentFilterManager
from swagger_server import util
from swagger_server.models_db.content_filter_db import ContentFilter as ContentFilter_db, UserContentFilter as UserContentFilter_db  # noqa: E501


def mib_resources_users_get_content_filter(user_id, filter_id):  # noqa: E501
    """mib_resources_users_get_content_filter

    Get the content filter # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int
    :param filter_id: Filter Unique ID
    :type filter_id: int

    :rtype: ContentFilterInfo
    """
    response_object = ContentFilterManager.retrieve_by_id_and_user(
        user_id, filter_id).first()
    return response_object.serialize()


def mib_resources_users_get_content_filters_list(user_id):  # noqa: E501
    """mib_resources_users_get_content_filters_list

    Get the list of available content filters # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: ContentFilter
    """
    response_object = ContentFilterManager.retrieve_list_by_user_id(
        user_id).first()
    return response_object.serialize()


def mib_resources_users_set_content_filter(user_id, filter_id):  # noqa: E501
    """Set the content filter flag to activate/disactivate it

     # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int
    :param filter_id: Filter Unique ID
    :type filter_id: int

    :rtype: ContentFilterInfo
    """
    content_filter = ContentFilterManager.retrieve_by_id_and_user(
        user_id, filter_id).first()
    if content_filter is None:
        new_user_content_filter = UserContentFilter_db()
        new_user_content_filter.filter_id = filter_id
        new_user_content_filter.filter_id_user = user_id
        new_user_content_filter.filter_active = True
        content_filter = ContentFilterManager.create_content_filter(
            new_user_content_filter)
    else:
        ContentFilterManager.toggle_content_filter(user_id, filter_id)
    return content_filter.serialize()
