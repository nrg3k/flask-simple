#!/usr/bin/env python
import logging
from app.api import flaskapi



def run_test_app():
    flaskapi.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    logging.debug("about to start flaskapi flask-app")
    run_test_app()
