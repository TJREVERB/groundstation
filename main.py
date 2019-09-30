from flask import Flask, request, jsonify

import functions

app = Flask(__name__)

@app.route("/send", methods=["POST"])
def handle_send():
    module, method, args = request.json["module"], request.json["method"], request.json["args"]
    functions.send(module, method, args)


if __name__ == '__main__':
    app.run()
