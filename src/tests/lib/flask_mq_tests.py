#!/usr/bin/env python
import logging
import os
import unittest
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from app.api import helpers as func


class TestSend(unittest.TestCase):

    def setup(self):
        logging.debug('setting up send messages')

    def tearDown(self):
        logging.debug('tearing down send message')

    # ---------cnb test cases---------#

if __name__ == '__main__':
    unittest.main()
