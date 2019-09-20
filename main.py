from flask import Flask, request

from tjgroundstationfunctions import *

'''
    BASIS FOR SEND MESSAGE HAS BEEN DEFINED
    NEEDS TO BE AESTHETICALLY BETTER
    NEED TO IMPLEMENT RECEIVE FUNCTIONS
    '''

moduleCheck = True
methodCheck = False
argsCheck = False
module = ""
method = ""
args = []
restart = False
enterStr = "Module"
messageStr = "Message Log:"
app = Flask(__name__)
#app.config["DEBUG"] = True

#@app.route("/", methods=["GET", "POST"])
@app.route("/", methods = ["GET", "POST"])
def adder_page():
    errors = ""
    global moduleCheck, methodCheck, argsCheck, module, method, args, restart, enterStr, messageStr
    if(restart == True):
        module = ""
        method = ""
        args = []
        restart = False
    if request.method == "POST":
        #try:
        number1 = str(request.form["number1"])
        #except:
        #errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        #try:
        #number2 = str(request.form["number2"])
        #except:
        #errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        if number1 is not None:
            print(moduleCheck, methodCheck)
            if(moduleCheck == True):
                result = in_module(number1)
                if(result == True):
                    moduleCheck = False
                    methodCheck = True
                    argsCheck = False
                    module = number1
                    enterStr = "method"
                    #result2 = in_method(number1, number2)
                    #if(result == True and result2 == True):
                    #send(number1, number2, ["Hi"])
                    return '''
                        <html>
                        <body>
                        {errors}
                        <p>{messageStr}</p>
                        <p>Enter your {enterStr}:</p>
                        <form method="post" action=".">
                        <p><input name="number1" /></p>
                        <p><input type="submit" value="Check" /></p>
                        </form>
                        <p>Module: {module}</p>
                        <p>Method: {method}</p>
                        <p>Arg List: {args}</p>
                        </body>
                        </html>
                        '''.format(errors=errors, enterStr = enterStr, module = module, method = method, args = args, messageStr = messageStr)
            if(methodCheck == True):
                print(module, number1)
                result = in_method(module, number1)
                if(result == True):
                    #print(result)
                    moduleCheck = False
                    methodCheck = False
                    argsCheck = True
                    method = number1
                    enterStr = "args"
                    #result2 = in_method(number1, number2)
                    #if(result == True and result2 == True):
                    #send(number1, number2, ["Hi"])
                    return '''
                        <html>
                        <body>
                        {errors}
                        <p>{messageStr}</p>
                        <p>Enter your {enterStr}:</p>
                        <form method="post" action=".">
                        <p><input name="number1" /></p>
                        <p><input type="submit" value="Check" /></p>
                        </form>
                        <p>Module: {module}</p>
                        <p>Method: {method}</p>
                        <p>Arg List: {args}</p>
                        </body>
                        </html>
                        '''.format(errors=errors, enterStr = enterStr, module = module, method = method, args = args, messageStr = messageStr)
            if(argsCheck == True):
                length = arg_length(module, method)
                args.append(number1)
                if(len(args) == length):
                    result = check_args(module, method, args)
                    if(result == True):
                        messageStr += "<br/>" + get_time() + get_message(module, method, args)
                        print(messageStr)
                        moduleCheck = True
                        methodCheck = False
                        argsCheck = False
                        restart = True
                        enterStr = "module"
                        send(module, method, args)
                        return '''
                            <html>
                            <body>
                            {errors}
                            <p>{messageStr}</p>
                            <p>Enter your {enterStr}:</p>
                            <form method="post" action=".">
                            <p><input name="number1" /></p>
                            <p><input type="submit" value="Check" /></p>
                            </form>
                            <p>Module: {module}</p>
                            <p>Method: {method}</p>
                            <p>Arg List: {args}</p>
                            <p>Message sent</p>
                            </body>
                            </html>
                            '''.format(errors=errors, enterStr = enterStr, module = module, method = method, args = args, messageStr = messageStr)
                    else:
                        args = []

    '''if(moduleCheck == True):
        enterStr = "module"
        elif(methodCheck == True):
        enterStr = "method"
        else:
        enterStr = "args"'''
    return '''
        <html>
        <body>
        {errors}
        <p>{messageStr}</p>
        <p>Enter your {enterStr}:</p>
        <form method="post" action=".">
        <p><input name="number1" /></p>
        <p><input type="submit" value="Check" /></p>
        </form>
        <p>Module: {module}</p>
        <p>Method: {method}</p>
        <p>Arg List: {args}</p>
        </body>
        </html>
        '''.format(errors=errors, enterStr = enterStr, module = module, method = method, args = args, messageStr = messageStr)

if __name__ == '__main__':
    app.run()
