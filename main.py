from flask import Flask, request, jsonify, render_template
from threading import Thread
import logging
import functions

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
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
def send():
    return render_template("index.html")


@app.route("/listen", methods=['GET'])
def listen():
    listen_list = myobject.get_list()
    for i in listen_list:
        if (listen_list[i].check_checksum is not True):
            failed_msg.append(i)
    myobject.reset_list()
    return jsonify(listen_list)

@app.route("/failed", methods=['GET'])
def checksum():
    return_list = failed_msg
    failed_msg.clear()
    return return_list
#returns all elements of failed_msg
#clears failed_msg
if __name__ == '__main__':
    '''t1 = Thread(target = listen_thread, args = ())
    t1.daemon = True
    t1.start()'''
    myobject = functions.listen_class([])
    myobject.start_listen()
    '''functions.start_listen()
    print(functions.get_time(), "yes")
    print("done")'''
    app.run()
