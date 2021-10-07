# run this file to start up gs
from flask import Flask, request, jsonify, render_template
import send
from listen import Listen

app = Flask(__name__)
@app.route("/send", methods=["POST"])
def handle_send():
    """
    Requests the module, method, and args from the front end
    Makes a request to the back end to send message
    """
    module, method, args = request.json["module"], request.json["method"], request.json["args"]
    if(send.in_module(module) and send.in_method(module, method) and send.check_args(module, method, args)):
        result = send.send(module, method, args)
        if result:
            return "message successfully sent", 200
        else:
            return "error in sending message", 500
    else:
        return "incorrect parameters", 405


@app.route("/")
def template():
    return render_template("index.html")


@app.route("/listen", methods=['GET'])
def listen():
    """
    Requests the listened messages from the backend
    Returns list of listened messages
    """
    listen_list = listen_object.get_list()
    listen_object.reset_list()
    return jsonify(listen_list), 200


if __name__ == '__main__':
    """
    Creates objcet of listen class and starts the listen thread
    Runs app
    """
    listen_object = Listen([])
    listen_object.start_thread()
    app.run()
