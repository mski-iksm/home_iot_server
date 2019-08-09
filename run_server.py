import yaml
import core.home_iot_server as iot
import flask
import logging
from _stat import filemode

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

with open('yamls/secret_server_setting.yml', 'r') as yf:
    server_settings = yaml.load(yf)


MYFORMAT = '[%(asctime)s]%(filename)s(%(lineno)d): %(message)s'
logging.basicConfig(
    filename='run.log',
    filemode='a',
    format=MYFORMAT,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


@app.route("/hello", methods=["get"])
def hello():
    response = {"message": "server running",
                "Content-Type": "application/json"}
    return flask.jsonify(response)


@app.route("/incoming", methods=["post"])
def incoming():
    response = {'message': 'not valid key',
                'text': 'NA',
                'Content-Type': 'application/json',
                }
    posted_data = flask.request.get_json()
    if posted_data['key'] == server_settings['key']:
        response['message'] = 'using valid key'
        response['text'] = posted_data['text'].replace(" ", "")
        logging.info(f'text: {posted_data["text"]}')
        signal, device, order = iot.make_signal(posted_data['text'])
        logging.info(f'device: {device}')
        logging.info(f'order: {order}')

    return flask.jsonify(response)


if __name__ == "__main__":
    print(" * Flask starting server...")

    app.run(
        port=server_settings['port'],
        ssl_context='adhoc',
        debug=False, host='0.0.0.0')
