import connexion
import six
from flask import json, jsonify

from swagger_server.models.content_filter import ContentFilter  # noqa: E501
from swagger_server.models.content_filter_info import ContentFilterInfo  # noqa: E501
from swagger_server.models.content_filter_info_put import ContentFilterInfoPUT  # noqa: E501
from swagger_server.models.purify_message import PurifyMessage  # noqa: E501
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
    if response_object is None:
        return jsonify({"message": "No content filter found"}), 404

    #words list is in json string format in the db. We do this for compatibility with ContentFilterInfo
    response_object[1].filter_words = json.loads(response_object[1].filter_words)
    return ContentFilterInfo.from_dict(response_object[0].serialize() | response_object[1].serialize()).to_dict()

def mib_resources_users_get_content_filters_list(user_id):  # noqa: E501
    """mib_resources_users_get_content_filters_list

    Get the list of available content filters # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: ContentFilter
    """
    response_object = ContentFilterManager.retrieve_list_by_user_id(
        user_id).first()
    if response_object is None:
        return jsonify({"message": "No content filter found"}), 404
    return ContentFilter.from_dict(response_object[0].serialize() | response_object[1].serialize()).to_dict()


def mib_resources_users_purify_message(body, user_id):  # noqa: E501
    """mib_resources_users_purify_message

    Purify a message # noqa: E501

    :param body: Create a new message and send it
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: PurifyMessage
    """
    if connexion.request.is_json:
        body = PurifyMessage.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def mib_resources_users_set_content_filter(body, user_id, filter_id):  # noqa: E501
    """Set the content filter flag to activate/disactivate it

     # noqa: E501

    :param body: Create a new message and send it
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int
    :param filter_id: Filter Unique ID
    :type filter_id: int

    :rtype: ContentFilterInfo
    """
    if connexion.request.is_json:
        body = ContentFilterInfoPUT.from_dict(connexion.request.get_json())  # noqa: E501
    
    content_filter :ContentFilter_db = ContentFilterManager.V2_get_filter_by_id(
        filter_id)
    
    user_content_filter :UserContentFilter_db = ContentFilterManager.V2_get_user_filter(filter_id, user_id)

    if content_filter.filter_private and user_content_filter is None:
        abort(403)

    if content_filter is None:
        abort(404)
    
    if user_content_filter is None and body.filter_active:
        user_content_filter = UserContentFilter_db()
        user_content_filter.filter_id = filter_id
        user_content_filter.filter_id_user = user_id
        user_content_filter.filter_active = body.filter_active
        ContentFilterManager.create_content_filter(user_content_filter)
    elif user_content_filter is not None:
        ContentFilterManager.V2_set_user_filter_status(user_content_filter, body.filter_active)

    return ContentFilterInfo.from_dict(content_filter.serialize() | user_content_filter.serialize()).to_dict()






        check_filter = ContentFilterManager.retrieve_by_id(filter_id).first()
        if check_filter is None:
            return jsonify({"message": "No content filter found"}), 404
        new_user_content_filter = UserContentFilter_db()
        new_user_content_filter.filter_id = filter_id
        new_user_content_filter.filter_id_user = user_id
        new_user_content_filter.filter_active = True
        ContentFilterManager.create_content_filter(
            new_user_content_filter)
        content_filter = ContentFilterManager.retrieve_by_id_and_user(
        user_id, filter_id).first()
    else:
        ContentFilterManager.toggle_content_filter(user_id,filter_id)
    content_filter[1].filter_words = json.loads(content_filter[1].filter_words)
    return ContentFilterInfo.from_dict(content_filter[0].serialize() | content_filter[1].serialize()).to_dict()
