import sys
import re
import os
import time
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from ...lib import logger
DEFAULT_CONFIG = {
    'user': os.environ['SMTP_USERNAME'],
    'pw': os.environ['SMTP_PASSWORD'],
    'mailhost': os.environ['SMTP_HOST'],
}
COMMASPACE = ', '

def send_email(recipients, subject, body, config=DEFAULT_CONFIG):
    try:
        s = smtplib.SMTP_SSL(config['mailhost'])
        s.ehlo()
        s.login(config['user'], config['pw'])
    except Exception as e:
        print("SMTP connect failed: {}".format(e))
        sys.exit(1)
    verified_recip = list()
    for email in recipients:
        if verify_address(email):
            verified_recip.append(email)
        else:
            logger.debug("rejecting email address: {}".format(email))

    msg = MIMEMultipart()
    msg['From'] = config['user']
    msg['To'] = COMMASPACE.join(verified_recip)
    msg['Subject'] = subject
    body = body + '\n\nThis is an automated email.'
    msg.attach(MIMEText(body, 'plain'))
    email_text = msg.as_string()

    try:
        s.sendmail(config['user'], COMMASPACE.join(verified_recip), email_text)
        s.close()
    except Exception as e:
        logger.error("Error sending email: {}").format(e)
        sys.exit(1)


def verify_address(email):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not EMAIL_REGEX.match(email):
        return 0
    else:
        return 1


def send_email_attachment(recipients, subject, body, filename=None, config=DEFAULT_CONFIG):
    if os.path.isfile(filename):
        _filename_ok = 1
    else:
        print("attachment file {} doesn't exist".format(filename))
        sys.exit(255)

    # TODO: add check of recipients list
    verified_recip = list()

    for email in recipients:
        if verify_address(email):
            verified_recip.append(email)
        else:
            logger.debug("rejecting email address: {}".format(email))
    try:
        s = smtplib.SMTP_SSL(config['mailhost'])
        s.ehlo()
        s.login(config['user'], config['pw'])
    except Exception as e:
        print("SMTP connect failed")
        sys.exit(1)

    msg = MIMEMultipart()
    msg['From'] = config['user']
    msg['To'] = COMMASPACE.join(verified_recip)
    msg['Subject'] = subject
    body = body + '\nPlease see attached file.\n\nThis is an automated email.'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename={}".format(os.path.basename(filename)))
    msg.attach(part)
    email_text = msg.as_string()

    try:
        s.sendmail(config['user'], COMMASPACE.join(verified_recip), email_text)
        s.close()
        ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print('[' + ts + '] DONE')
    except Exception as e:
        print("Error sending email: {}".format(e))
        sys.exit(1)
