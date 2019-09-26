from flask import Flask, request

from functions import *

'''
    BASIS FOR SEND MESSAGE HAS BEEN DEFINED
    NEEDS TO BE AESTHETICALLY BETTER
    NEED TO IMPLEMENT RECEIVE FUNCTIONS
    '''

submodString = "<font color=green> <b>Modules:</b></br> adcs</br>eeprom</br>imu</br>serial</br>aprs</br>init</br>sys</br>eps</br>iridium</br>telemetry</br>gps</br>radio_output</br>time</br>command_ingest</br>housekeeping</br>_init_ </font>"
errors = ""
moduleCheck = True
methodCheck = False
argsCheck = False
module = ""
method = ""
args = []
restart = False
enterStr = "Module"
messageStr = "<b>Message Log:</b> </br>"
messageStr += submodString + "<font color=blue></br><b>Which module: </b></font>"
print()


def return_template(errors, enterStr, module, method, args, messageStr):
    template = '''
                <html>
                <body>
                {errors}
                <div style="width: 600px; height: 700px; overflow-y: scroll;"> {messageStr}</div>
                <p>Enter your {enterStr}:</p>
                <form method="post" action=".">
                <p><input name="number1" /></p>
                <p><input type="submit" value="Check" /></p>
                </form>
                </body>
                </html>
                '''.format(errors=errors, enterStr=enterStr, module=module, method=method, args=args,
                           messageStr=messageStr)
    return (template)


app = Flask(__name__)


# app.config["DEBUG"] = True

# @app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def adder_page():
    global moduleCheck, methodCheck, argsCheck, module, method, args, restart, enterStr, messageStr, errors
    if (restart == True):
        module = ""
        method = ""
        args = []
        restart = False
    if request.method == "POST":
        # try:
        number1 = str(request.form["number1"])
        # except:
        # errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        # try:
        # number2 = str(request.form["number2"])
        # except:
        # errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        if number1 is not None:
            print(moduleCheck, methodCheck)
            if (moduleCheck == True):
                result = in_module(number1)
                if (result == True):
                    moduleCheck = False
                    methodCheck = True
                    argsCheck = False
                    module = number1
                    enterStr = "method"
                    messageStr += module + print_Methods(module) + "<font color=blue><b>Which method: </b></font>"
                    # result2 = in_method(number1, number2)
                    # if(result == True and result2 == True):
                    # send(number1, number2, ["Hi"])
                    return return_template(errors, enterStr, module, method, args, messageStr)
            if (methodCheck == True):
                print(module, number1)
                result = in_method(module, number1)
                if (result == True):
                    # print(result)
                    moduleCheck = False
                    methodCheck = False
                    argsCheck = True
                    method = number1
                    enterStr = "args"
                    messageStr += method + get_arg(module, method) + "<font color=blue><b></br>Enter args: </b></font>"
                    # result2 = in_method(number1, number2)
                    # if(result == True and result2 == True):
                    # send(number1, number2, ["Hi"])
                    return return_template(errors, enterStr, module, method, args, messageStr)
            if (argsCheck == True):
                length = arg_length(module, method)
                args.append(number1)
                messageStr += "</br>" + number1
                if (len(args) == length):
                    result = check_args(module, method, args)
                    if (result == True):
                        messageStr += "<br/><font color=black><b>" + get_time() + get_message(module, method,
                                                                                              args) + "</b></br></br><font>"
                        messageStr += submodString + "</br><font color=blue><b>Which module: </b></font>"
                        print(messageStr)
                        moduleCheck = True
                        methodCheck = False
                        argsCheck = False
                        restart = True
                        enterStr = "module"
                        send(module, method, args)
                        return return_template(errors, enterStr, module, method, args, messageStr)
                    else:
                        args = []
                else:
                    return (return_template(errors, enterStr, module, method, args, messageStr))

    '''if(moduleCheck == True):
        enterStr = "module"
        elif(methodCheck == True):
        enterStr = "method"
        else:
        enterStr = "args"'''
    return return_template(errors, enterStr, module, method, args, messageStr)


if __name__ == '__main__':
    app.run()
