from functools import update_wrapper
from typing import List
import connexion
import six
from flask import json, jsonify, abort

from swagger_server.models.content_filter import ContentFilter  # noqa: E501
from swagger_server.models.content_filter_info import ContentFilterInfo  # noqa: E501
from swagger_server.models.content_filter_info_put import ContentFilterInfoPUT  # noqa: E501
from swagger_server.models.purify_message import PurifyMessage  # noqa: E501
from swagger_server.dao.content_filter_manager import ContentFilterManager
from swagger_server import util
from swagger_server.models_db.content_filter_db import ContentFilter as ContentFilter_db, UserContentFilter as UserContentFilter_db  # noqa: E501
import re

def mib_resources_users_get_content_filter(user_id, filter_id):  # noqa: E501
    """mib_resources_users_get_content_filter

    Get the content filter # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int
    :param filter_id: Filter Unique ID
    :type filter_id: int

    :rtype: ContentFilterInfo
    """
    content_filter = ContentFilterManager.V2_get_filter_by_id(filter_id)
    user_content_filter = ContentFilterManager.V2_get_user_filter(filter_id, user_id)
    if content_filter is None:
        abort(404)
    content_filter.filter_words = json.loads(content_filter.filter_words)
    mixed = (user_content_filter.serialize() | content_filter.serialize()) if user_content_filter is not None else content_filter.serialize()

    #words list is in json string format in the db. We do this for compatibility with ContentFilterInfo
    return ContentFilterInfo.from_dict(mixed).to_dict() 

def mib_resources_users_get_content_filters_list(user_id):  # noqa: E501
    """mib_resources_users_get_content_filters_list

    Get the list of available content filters # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: List[ContentFilter]
    """
    results = ContentFilterManager.retrieve_list_by_user_id(user_id)
    content_list = []
    for result in results:
        user_content_filter :UserContentFilter_db = result.UserContentFilter
        content_filter :ContentFilter_db = result.ContentFilter

        content_filter.filter_words = []
        mixed = (user_content_filter.serialize() | content_filter.serialize()) if user_content_filter is not None else content_filter.serialize()
        
        content_list.append(ContentFilter.from_dict(mixed).to_dict())
        #content_list.append(ContentFilterInfo.from_dict({'filter_id':result.ContentFilter.filter_id,'filter_name':result.ContentFilter.filter_name,'filter_active':True if result.UserContentFilter and
        #                            result.UserContentFilter.filter_active else False}).to_dict())
    
    return content_list

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
    
    personal_filters = ContentFilterManager.retrieve_list_by_user_id(user_id)

    purified_message = body.text

    for personal_filter in personal_filters:
        if personal_filter.UserContentFilter.filter_active:
            for word in json.loads(personal_filter.ContentFilter.filter_words):
                insensitive_word = re.compile(re.escape(word), re.IGNORECASE)
                purified_message = insensitive_word.sub('*' * len(word), purified_message)

    purify_message :PurifyMessage = PurifyMessage()
    purify_message.text = purified_message

    return purify_message.to_dict()


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

    if content_filter is None:
        abort(404)

    if content_filter.filter_private and user_content_filter is None:
        abort(403)
    
    
    if user_content_filter is None and body.filter_active:
        user_content_filter = UserContentFilter_db()
        user_content_filter.filter_id = filter_id
        user_content_filter.filter_id_user = user_id
        user_content_filter.filter_active = body.filter_active
        ContentFilterManager.create_content_filter(user_content_filter)
    elif user_content_filter is not None:
        ContentFilterManager.V2_set_user_filter_status(user_content_filter, body.filter_active)
    content_filter.filter_words = json.loads(content_filter.filter_words)
    
    mixed = (user_content_filter.serialize() | content_filter.serialize()) if user_content_filter is not None else content_filter.serialize()
    return ContentFilterInfo.from_dict(mixed).to_dict()
