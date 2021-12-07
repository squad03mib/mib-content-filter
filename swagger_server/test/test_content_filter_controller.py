# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.purify_message import PurifyMessage  # noqa: E501
from swagger_server.models.content_filter import ContentFilter  # noqa: E501
from swagger_server.models.content_filter_info import ContentFilterInfo  # noqa: E501
from swagger_server.models.content_filter_info_put import ContentFilterInfoPUT
from swagger_server.test import BaseTestCase
import unittest

class TestContentFilterController(BaseTestCase):
    """ContentFilterController integration test stubs"""
    
    def test_content_filter_1(self):
        """Test case for mib_resources_users_set_content_filter
        """
        body = ContentFilterInfoPUT()
        body.filter_active = True
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=1, filter_id=1),data=json.dumps(body.to_dict()),
                content_type='application/json',
                method='PUT')
        assert response.status_code == 200

    def test_content_filter_2(self):
        """Test case for mib_resources_users_get_content_filter
        """
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=1, filter_id=1),
            method='GET')
        assert response.status_code == 200

    def test_content_filter_3(self):
        """Test case for mib_resources_users_get_content_filters_list
        """
        response = self.client.open(
            '/users/{user_id}/content_filter'.format(user_id=1),
            method='GET')
        assert response.status_code == 200

    def test_content_filter_4(self):
        """Test case for mib_resources_users_get_content_filters_list
        
        """
        response = self.client.open(
            '/users/{user_id}/content_filter'.format(user_id=10),
            method='GET')
        assert response.status_code == 200
    
    def test_content_filter_5(self):
        """Test case for mib_resources_users_get_content_filter
            
        """
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=11, filter_id=1),
            method='GET')
        assert response.status_code == 200
    def test_content_filter_5(self):
        """Test case for mib_resources_users_get_content_filter
            content filter that doesn't exist
        """
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=1, filter_id=11),
            method='GET')
        assert response.status_code == 404
    def test_content_filter_6(self):
        """Test case for mib_resources_users_set_content_filter
            content filter that doesn't exist
        """
        body = ContentFilterInfoPUT()
        body.filter_active = True
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=1, filter_id=11),data=json.dumps(body.to_dict()),
                content_type='application/json',
                method='PUT')
        assert response.status_code == 404
    def test_content_filter_7(self):
        '''Test case for mib_resources_users_purify_message
        '''
        body = PurifyMessage()
        body.text = "hi fuck"
        response = self.client.open(
            '/users/{user_id}/content_filter/purify_message'.format(
                user_id=1),data=json.dumps(body.to_dict()),
                content_type='application/json',
                method='POST')
        assert response.status_code == 200
    def test_content_filter_8(self):
        """Test case for mib_resources_users_set_content_filter
            content filter that doesn't exist
        """
        body = ContentFilterInfoPUT()
        body.filter_active = False
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=1, filter_id=1),data=json.dumps(body.to_dict()),
                content_type='application/json',
                method='PUT')
        assert response.status_code == 200
