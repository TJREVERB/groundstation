from flask import Flask
app = Flask(__name__)


@app.route("/")
def main():
    return "Hello, world!"


@app.route("/send", methods=["POST"])
def send():
    return "COOL"


var = [int, str]
var1 = 1
if isinstance(var1, int):
    print("GOODO")

if __name__ == "__main__":
    app.run()
