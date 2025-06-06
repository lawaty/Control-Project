import os
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv

from DemoPack.DemoUnit import Demo

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return """Available Routes:\n
/<param>: Demo Route
"""

demo = Demo()
@app.route("/<param>")
def demoEndpoint(param):
    demo.run(param)
    return "Demo Run Successfully"

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host=host, port=port, debug=True)
