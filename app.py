import os
# import flask
from flask import Flask
import models
from resources.users import users
from resources.groups import groups
from resources.members import members
from resources.messages import messages
from resources.players import players
# this is the main tool for coordinating the login/session
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room



# print the error
DEBUG = True
PORT = 8000


app = Flask(__name__)
# set up a secret key
app.secret_key = "kdkjflseinoirnspp23dk3odkcm9m"
# add Flask-SocketIO to the Flask application
socketio = SocketIO(app, cors_allowed_origins=['https://socialcommunity.herokuapp.com', 'http://localhost:3000'])


# instantiate LoginManager to a login_manager
login_manager = LoginManager()

# connect the app to login_manager
login_manager.init_app(app)


# user loader will use this callback to load the user object
@login_manager.user_loader
def load_user(user_id):

	try:
		# look up user
		return models.User.get(models.User.id == user_id)

	except models.DoesNotExist:
		return None


CORS(users, origins=['http://localhost:3000', 'https://socialcommunity.herokuapp.com'], supports_credentials=True)
CORS(groups, origins=['http://localhost:3000', 'https://socialcommunity.herokuapp.com'], supports_credentials=True)
CORS(members, origins=['http://localhost:3000', 'https://socialcommunity.herokuapp.com'], supports_credentials=True)
CORS(messages, origins=['http://localhost:3000', 'https://socialcommunity.herokuapp.com'], supports_credentials=True)
CORS(players, origins=['http://localhost:3000', 'https://socialcommunity.herokuapp.com'], supports_credentials=True)




# use the blueprint that will handle the users stuff
app.register_blueprint(users, url_prefix='/api/v1/users/')
app.register_blueprint(groups, url_prefix='/api/v1/groups/')
app.register_blueprint(members, url_prefix='/api/v1/members/')
app.register_blueprint(messages, url_prefix='/api/v1/messages/')
app.register_blueprint(players, url_prefix='/api/v1/players/')


# join a room
@socketio.on('join')
def on_join(data):
    room = data['room']
    print('someone joined room: ', room)
    join_room(room)

# leave a room
@socketio.on('leave')
def on_leave(data):
    room = data['room']

    print('someone is leaving room: ', room)
    leave_room(room)
    close_room(room, namespace=room)

# send message
@socketio.on('message')
def handle_message(message):

    print('printing message')
    print(message)
    send(message, broadcast=True)
    return None


# ADD THESE THREE LINES -- because in production the app will be run with 
# gunicorn instead of by the three lines below, so we want to initialize the
# tables in that case as well
if 'ON_HEROKU' in os.environ: 
    print('\non heroku!')
    models.initialize()




if __name__ == '__main__':
	models.initialize()
	socketio.run(app, debug=DEBUG, port=PORT)
