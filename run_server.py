import flask
app = flask.Flask(__name__)


@app.route("/hello", methods=["get"])
def hello():
    response = {"message": "server running",
                "Content-Type": "application/json"}
    return flask.jsonify(response)


if __name__ == "__main__":
    print(" * Flask starting server...")
    app.run()
