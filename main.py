from flask import Flask, request, jsonify, render_template
from threading import Thread
import functions

app = Flask(__name__)
message = []
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
    '''global message
    print("Started listen thread")
    functions.start_listen()
    print("message recieved")'''
    # print(functions.start_listen())
    # unctions.start_listen()
    listen_list = myobject.get_list()
    myobject.reset_list()
    return jsonify(listen_list)
    '''if(functions.messageList == []):
        return("No message found")
    else:
        print(functions.messageList[-1])
        return(functions.messageList[-1])'''

    '''global message
    while True:
        messageStr = functions.listen()
        if messageStr is not None:
            message.append(messageStr)'''

    #Thread(target=functions.listen, daemon=True).start()
    '''listenMessage = functions.listen()
    print(listenMessage)
    return(listenMessage)'''

    # global message
    # return message[-1]
    # functions.list
'''
def listen_thread():
    global message
    print("Started listen thread")
    return("hi")'''
'''while True:
        messageStr = functions.listen()
        """
        if messageStr is not None:
            message.append(messageStr)
        else:
            message.append("nothing here")
        """
        message.append("test")
        print(message)'''

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
