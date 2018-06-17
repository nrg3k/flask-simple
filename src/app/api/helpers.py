"""Helper methods common to all api entry points"""
import uuid
import functools
import datetime
import os
import pika
import rapidjson
from flask import g
from flask import Response
from flask import json
from ..lib import logger
from ..lib import constants as FLASKAPI


def no_handler():
    err = error_message(FLASKAPI.ERRORS['CHANNEL_NOT_SUPPORTED'],
                        'Channel is not supported')
    return failure([err], status_code=400)


def error_message(code, msg, field=''):
    return {
        'code': code,
        'message': msg,
        'field': field
    }


def success(data, status_code=200, **kwargs):  # pragma: no cover
    _resp = {
        'status': kwargs.get('status', 'success'),
        'data': data,
        'message': kwargs.get('message', '')
    }

    return Response(json.dumps(_resp), status_code, mimetype='application/json')


def failure(data, status_code=400, **kwargs):  # pragma: no cover
    _resp = {
        'status': kwargs.get('status', 'error'),
        'errors': data,
        'message': kwargs.get('message', '')
    }

    return Response(json.dumps(_resp), status_code, mimetype='application/json')


def _response_from_dict(_resp, status_code, **kwargs):
    json = rapidjson.dumps(_resp, datetime_mode=rapidjson.DM_ISO8601 | rapidjson.DM_NAIVE_IS_UTC,
                           number_mode=rapidjson.NM_DECIMAL)

    return Response(json, mimetype='application/json', status=status_code)


def generate_id():
    return uuid.uuid4()


def missing_fields_response(fields):
    errors = [error_message(FLASKAPI.ERRORS['MISSING_REQUIRED'],
                            'Missing required field',
                            field=field)
              for field in fields]
    return failure(errors)


def validation(*required_args):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            missing = [k for k in required_args if k not in g.params]
            if missing:
                return missing_fields_response(missing)
            return f(*args, **kwargs)

        return wrapper

    return decorator


def add_to_queue(queue, message):
    mq_url = 'amqp://' + os.environ.get('MQ_USERNAME') + ':' + os.environ.get('MQ_PASSWORD') + '@' \
             + os.environ.get('MQ_HOST') + ':' + os.environ.get('MQ_PORT') + '/%2F'
    parameters = pika.URLParameters(mq_url)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    logger.info("adding {} to queue".format(message))

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    logger.info(channel.basic_publish)
    connection.close()
    return "Sent %r" % message + " to Queue: %r" % queue


def write_csv_output(data, filename):
    fieldnames = list()
    for f in data[0].keys():
        fieldnames.append(f)
    logger.debug(fieldnames)
    output_path = "/tmp/" + filename
    with open(file=output_path, mode='w') as csvfile:
        output = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        output.writeheader()
        for row in data:
            output.writerow(row)


def slack_notify(message):
    slackURL = os.environ.get('SLACK_WEBHOOK')
    slackpayload = {
        "fallback": message,
        "color": "#36a64f",
        "fields": [
            {
                "title": "Flask API Report",
                "value": message,
                "short": 'false'
            }
        ]
    }
    postdata = {'payload': json.dumps(slackpayload)}
    r = requests.post(slackURL, data=postdata)
    return r.text


def uniqid(prefix=''):
    return prefix + hex(int(time()))[2:10] + hex(int(time() * 1000000) % 0x100000)[2:7]



