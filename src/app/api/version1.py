#!/usr/bin/env python

import json
import os
import re
from ..lib import logger
from flask import g
from ..lib import constants as FLASKAPI
from . import helpers as api
from flask import request, Blueprint
from flask import Blueprint
from .helpers import add_to_queue

v1 = Blueprint('routes', __name__)

@v1.route('/', methods=['GET'])
def api_home():
    logger.info("Generic homepage route for v1")
    return "Generic homepage route for v1"

# --- error code indexes --- #
@v1.errorhandler(404)
def page_not_found(e):
    return '404 error {}'.format(e), 404


@v1.errorhandler(500)
def internal_server_error(e):
    return '500 error {} '.format(e), 500


@v1.errorhandler(502)
def bad_gateway_error(e):
    return '502 error {}'.format(e), 502


@v1.errorhandler(504)
def gateway_timeout_error(e):
    return '504 error {}'.format(e), 504


@v1.errorhandler(505)
def bad_gateway_error(e):
    return '505 error {} '.format(e), 505
