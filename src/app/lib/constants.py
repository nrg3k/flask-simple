# -*- coding: utf-8 -*-
import os
LOG_FORMAT = "%(asctime)s %(name)s@{}s [%(process)d] %(levelname)-8s %(message)s [in %(pathname)s:%(funcName)s:%(lineno)d]".format(os.getenv('HOSTNAME'))
LOG_DATE_FORMAT = '%m-%d %H:%M'



DEV_FLAG = 'DEV'
DEV_MQ_SLEEP = 30 # seconds

PROD_FLAG = 'PROD'

ERRORS = {
    'UNSUPPORTED': 1001,
    'MISSING_REQUIRED': 2000,
    'CHANNEL_NOT_SUPPORTED': 5000,
    'MISSING_META': 10000,
    'INTERNAL_CONNECTION_ERROR': 10001,
    'MISSING_BUCKET_NAME': 130001,
    'MISSING_FILE_NAME': 140000,
    'INTERNAL_SERVER_ERROR':140001
}

SERVICE_NAME = 'flaskapi'
DEFAULT_EMAIL = 'reports@company.com'


