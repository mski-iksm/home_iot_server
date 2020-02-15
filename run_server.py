#!/usr/local/bin/python3.6
import yaml
import logging

import flask

from core.home_iot_server import get_server_settings
from core.set_server import setup_app
# from _stat import filemode

MYFORMAT = '[%(asctime)s]%(filename)s(%(lineno)d): %(message)s'
logging.basicConfig(filename='run.log', filemode='a', format=MYFORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

setup_app(app)

if __name__ == '__main__':
    print('**** Flask starting server ****')

    server_settings = get_server_settings()
    app.run(port=server_settings['port'], ssl_context='adhoc', debug=False, host='0.0.0.0')
