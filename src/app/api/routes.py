import sys, os
from flask import g
from flask import request

from . import flaskapi
from . import helpers as api

from ..lib import logger
from ..lib import constants as FLASKAPI
#from ..lib.services import database as edb

DO_NOT_CHECK = []

#DB = edb.GenericDB()

def _standardize_params(params):
    if not params:
        params = {}
    if 'channel' not in params:
        params['channel'] = ''
    if 'lang_code' not in params:
        params['lang_code'] = ''
    if 'country_code' not in params:
        params['country_code'] = ''
    return params


#
# Api Requirements
#
@flaskapi.before_request
def api_requires():
    logger.debug("Setting up request")
    params = []

    if request.method in ('GET', 'DELETED'):
        # request.args is an ImmutableMultiDict
        params = request.args.copy()

    elif request.method == 'POST':
        if request.is_json:
            params = request.get_json(silent=True)
        else:
            params = request.form.copy()

    g.params = _standardize_params(params)

    if request.url_rule:
        g.params['uri_rule'] = request.url_rule.rule

    g.params['uri_endpoint'] = request.endpoint

@flaskapi.route('/', methods=['GET'])
def default_home():
    logger.info("Generic homepage route")
    return "Generic homepage route"

#
# Health Check
#
@flaskapi.route('/service/health')
def health_check():
    logger.info('health check')
    return api.success({'msg': 'All systems are up'})


@flaskapi.route('/service/database_health')
def database_health_check():
    logger.info('health check')
    params = {'param': None}
    sql = """select version()"""
    res = edb.execute_read(DB.read_connection(), sql, params)
    print(res)
    return api.success({'msg': res})

