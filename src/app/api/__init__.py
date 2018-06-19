import os
import datadog
from . import version1
from flask import Flask  # pragma: no cover
from ..lib import logger

from . import version1

datadog_options = {
    'statsd_host': os.environ.get('STATSD_HOST', 'statsd.monitoring'),
    'statsd_port': os.environ.get('STATSD_PORT', '8125')
}

datadog.initialize(**datadog_options)
logger.debug("statsd initialized")

flaskapi = Flask(__name__)
flaskapi.register_blueprint(version1.v1, url_prefix='/v1')
logger.info("flaskapi started")

from . import routes

