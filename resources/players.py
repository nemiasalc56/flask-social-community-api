# import our models and blueprint
import models
from flask import Blueprint, request


players = Blueprint('players', 'players')



# create route
@players.route('/', methods=['POST'])
def player():

	# get the information from the request
	payload = request.get_json()
	print(payload)

	return "You hit the players create route"