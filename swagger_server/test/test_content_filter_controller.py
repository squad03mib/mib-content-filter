# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.content_filter import ContentFilter  # noqa: E501
from swagger_server.models.content_filter_info import ContentFilterInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestContentFilterController(BaseTestCase):
    """ContentFilterController integration test stubs"""

    def test_mib_resources_users_get_content_filter(self):
        """Test case for mib_resources_users_get_content_filter


        """
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=789, filter_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_content_filters_list(self):
        """Test case for mib_resources_users_get_content_filters_list


        """
        response = self.client.open(
            '/users/{user_id}/content_filter'.format(user_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_set_content_filter(self):
        """Test case for mib_resources_users_set_content_filter

        Set the content filter flag to activate/disactivate it
        """
        response = self.client.open(
            '/users/{user_id}/content_filter/{filter_id}'.format(
                user_id=789, filter_id=789),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
