# import flask
from flask import Flask
import models
from resources.users import users
# this is the main tool for coordinating the login/session
from flask_login import LoginManager




# print the error
DEBUG = True
PORT = 8000


app = Flask(__name__)


# set up a secret key
app.secret_key = "kdkjflseinoirnspp23dk3odkcm9m"

# instantiate LoginManager to a login_manager
login_manager = LoginManager()

# connect the app to login_manager
login_manager.init_app(app)





# use the blueprint that will handle the users stuff
app.register_blueprint(users, url_prefix='/api/v1/users/')













if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)