# import models and blueprint
import models
from flask import Blueprint, request




# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# register create route
@users.route('/register', methods=['POST'])
def register():
	# get the info from the request
	payload = request.get_json()
	print(payload)

	return "You hit the register route"