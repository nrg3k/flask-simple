"""Module for working with our mysql db connections"""
# -*- coding: utf-8 -*-
import os, sys
import traceback
import MySQLdb
import MySQLdb.cursors
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from ...lib import logger

DB_CONFIG = {
    'db_name': os.environ.get('DB_DATABASE', ''),
    'read_username': os.environ.get('READ_DB_USERNAME', ''),
    'read_password': os.environ.get('READ_DB_PASSWORD', ''),
    'read_host': os.environ.get('READ_DB_HOST', ''),
    'read_port': int(os.environ.get('READ_DB_PORT', 3306)),
    'write_username': os.environ.get('WRITE_DB_USERNAME', ''),
    'write_password': os.environ.get('WRITE_DB_PASSWORD', ''),
    'write_host': os.environ.get('WRITE_DB_HOST', ''),
    'write_port': int(os.environ.get('WRITE_DB_PORT', 3306))
}


def execute_write(conn, query, params=None):
    result = None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        result = cursor.lastrowid or cursor.rowcount or None

    except Exception as err:  # pragma: no cover
        logger.exception("DB execute_write Write Exception: {}".format(err))
        logger.exception(traceback.format_exc())
        conn.rollback()

    finally:
        logger.debug("DB Write query: {}".format(query))
        logger.debug("DB write params: {}".format(params))
        if cursor:
            cursor.close()

    return result


def execute_write_insert(conn, query, params=None):
    result = None

    try:
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()
        result = cursor.rowcount or None

    except Exception as err:  # pragma: no cover
        logging.exception("DB execute_write_insert Write Exception: {}".format(err))
        logging.exception(traceback.format_exc())
        conn.rollback()

    finally:
        # logging.info("DB Write query: {}".format(query))
        logger.debug("DB Write query: {}".format(query))
        logger.debug("DB write params: {}".format(params))
        if cursor:
            cursor.close()

    return result


def execute_read(conn, query, params, only_one=False):
    result = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)

        if only_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

    except Exception as err:  # pragma: no cover
        logger.exception("DB execute_read Exception: {}".format(err))
        logger.exception(traceback.format_exc())

    finally:
        logger.debug("DB Read query: {}".format(query))
        logger.debug("DB Read params: {}".format(params))
        logger.debug("DB Read only_one: {}".format(only_one))
        if cursor:
            cursor.close()

    return result


#
# Database classes
#
class BaseDB(object):

    def __init__(self, config, **kwargs):
        self.read_conn = None
        self.write_conn = None
        self.config = config

    def read_connection(self):
        if not self.is_open(self.read_conn):
            username = self.config.get('read_username', None)
            password = self.config.get('read_password', None)
            host = self.config.get('read_host', None)
            port = self.config.get('read_port', None)
            dbname = self.config.get('db_name', None)
            self.read_conn = self.__connect(username, password, host, port, dbname)

        return self.read_conn

    def write_connection(self):
        if not self.is_open(self.write_conn):
            username = self.config.get('write_username', None)
            password = self.config.get('write_password', None)
            host = self.config.get('write_host', None)
            port = self.config.get('write_port', None)
            dbname = self.config.get('db_name', None)
            self.write_conn = self.__connect(username, password, host, port, dbname)
        return self.write_conn

    def is_open(self, connection):
        try:
            with connection.cursor():
                return True
        except (AttributeError, MySQLdb.ProgrammingError):
            pass
        return False

    def close(self):
        if self.read_conn:
            self.read_conn.close()
        if self.write_conn:
            self.write_conn.close()

    def __connect(self, username, password, host, port, dbname,
                  **kwargs):
        conn = None
        cursor_type = kwargs.get('cursor_type', MySQLdb.cursors.DictCursor)

        try:
            conn = MySQLdb.connect(host=host, port=port, user=username,
                                   passwd=password, db=dbname,
                                   cursorclass=cursor_type)
        except MySQLdb.InterfaceError:  # pragma: no cover
            logging.fatal('BaseDB unable to create DB conn!')
            logging.fatal(traceback.format_exc())

        return conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class GenericDB(BaseDB):
    """Shortcut class for Channel DB connections"""

    def __init__(self, **kwargs):
        config = kwargs.get('config') or DB_CONFIG
        super(GenericDB, self).__init__(config, **kwargs)


