# import flask
from flask import Flask



# print the error
DEBUG = True
PORT = 8000


app = Flask(__name__)













if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)