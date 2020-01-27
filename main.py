from flask import Flask, request, jsonify, render_template
from threading import Thread
import logging
import functions

app = Flask(__name__)
message = []
failed_msg = [] #list of every message that has an incorrect checksum
@app.route("/send", methods=["POST"])
def handle_send():
    module, method, args = request.json["module"], request.json["method"], request.json["args"]
    print(module, method, args)
    if(functions.in_module(module) and functions.in_method(module, method) and functions.check_args(module, method, args)):
        result = functions.send(module, method, args)
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
    listen_list = listenObject.get_list()
    #for i in listen_list:
        #if (listen_list[i].check_checksum is not True):
            #failed_msg.append(i)
    listenObject.reset_list()
    return jsonify(listen_list)

@app.route("/failed", methods=['GET'])
def checksum():
    return_list = failed_msg
    failed_msg.clear()
    return return_list

if __name__ == '__main__':
    listenObject = functions.listen_class([])
    listenObject.start_listen()
    app.run()
