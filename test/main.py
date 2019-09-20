from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    #if request.method == "POST":
    #    #if number1 is not None and number2 is not None:
    #    #result = do_calculation(number1, number2)
    #    return '''
    #        <html>
    #            <body>
    #                <p>The result is {result}</p>
    #                <p><a href="/">Click here to calculate again</a>
    #            </body>
    #        </html>
    #    '''.format(result="Hello")
    if request.method == "POST":
        return '''
            <html>
                <body>
                    {errors}
                    <form method="post" action=".">
                        <p><input type="submit" value="Refresh" /></p>
                    </form>
                </body>
            </html>
        '''.format(errors=errors)
    return '''
        <html>
            <body>
                {errors}
                <form method="post" action=".">
                    <p><input type="submit" value="Refresh" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)
if __name__ == '__main__':
    app.run()
