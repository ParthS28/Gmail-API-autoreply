import os, sys
from flask import Flask, request

app = Flask(__name__)
@app.route('/', methods=['GET'])

if __name__ == "__main__":
	app.run(debug = True, port = 5000)