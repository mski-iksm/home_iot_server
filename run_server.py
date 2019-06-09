import yaml
import core.home_iot_server as iot
import flask
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

with open('yamls/secret_server_setting.yml', 'r') as yf:
    server_settings = yaml.load(yf)


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
        response['text'] = posted_data['text']
        iot.make_signal(posted_data['text'])

    return flask.jsonify(response)


if __name__ == "__main__":
    print(" * Flask starting server...")

    app.run(
        port=server_settings['port'],
        ssl_context='adhoc',
        debug=False, host='0.0.0.0')
