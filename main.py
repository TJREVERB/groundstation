from flask import Flask, request

from tjgroundstationfunctions import *

'''
CURRENTLY JUST CHECKS IF MODULE AND METHOD ARE VALID
NEEDS TO PROMPT ARGS FOR METHOD THEN CHECK ARGS (check_args(module, method, arglist))
THEN SEND MESSAGE
NEEDS TO DISPLAY PREVIOUS METHODS
DISPLAY LISTENED MESSAGES
'''


app = Flask(__name__)
#app.config["DEBUG"] = True

#@app.route("/", methods=["GET", "POST"])
@app.route("/", methods = ["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        #try:
        number1 = str(request.form["number1"])
        #except:
            #errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        #try:
        number2 = str(request.form["number2"])
        #except:
            #errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        if number1 is not None:
            result = in_module(number1)
            result2 = in_method(number1, number2)
            #if(result == True and result2 == True):
            #send(number1, number2, ["Hi"])
            return '''
                <html>
                    <body>
                        <p>The module is {number1}</p>
                        <p>The method is {number2}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(number1=result, number2 = result2)
             

    return '''
        <html>
            <body>
                {errors}
                <p>Enter your module and method:</p>
                <form method="post" action=".">
                    <p><input name="number1" /></p>
                    <p><input name="number2" /></p>
                    <p><input type="submit" value="Do calculation" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

if __name__ == '__main__':
    app.run()
