#!/usr/bin/env python
import logging
import os
import unittest
import sys

# Set the path for our application
# sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

#from app.lib.services import database


class TestDatabase(unittest.TestCase):  # pylint: disable=r0904
    """Tests the events module"""

    def setUp(self):
        """Sets up before each test"""
        logging.debug('setting up TestServiceSearch')

    def tearDown(self):
        """Tears down after each test"""
        logging.debug('tearing down TestServiceSearch')

    def testConnection1(self):
        assert True


if __name__ == '__main__':
    unittest.main()  # pragma: no cover





