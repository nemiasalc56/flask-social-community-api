# import flask
from flask import Flask
import models
from resources.users import users



# print the error
DEBUG = True
PORT = 8000


app = Flask(__name__)



# use the blueprint that will handle the users stuff
app.register_blueprint(users, url_prefix='/api/v1/users/')













if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)