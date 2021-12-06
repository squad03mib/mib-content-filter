import logging

import connexion
from flask_testing import TestCase
import unittest


class BaseTestCase(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from swagger_server import create_app
        app = create_app()
        cls.client = app.test_client()

