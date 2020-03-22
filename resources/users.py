# import models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_user
from flask_bcrypt import generate_password_hash




# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# register create route
@users.route('/register', methods=['POST'])
def register():
	# get the info from the request
	payload = request.get_json()
	print(payload)

	# make the email lowercase
	payload['email'] = payload['email'].lower()

	# check if the user already exists by checking their email.
	try:
		models.User.get(models.User.email == payload['email'])

		# if it does not, inform the user

		return jsonify(
			data={},
			message=f"A user the the email {payload['email']} already exists",
			status=401
			), 401


	except models.DoesNotExist:
		# if it does not, we can proceed
		new_user = models.User.create(
			first_name = payload['first_name'],
			last_name = payload['last_name'],
			picture = payload['picture'],
			email = payload['email'],
			password = generate_password_hash(payload['password'])
			)
	

		# convert mode to dictionary
		user_dict = model_to_dict(new_user)
		print(user_dict)

		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"Succesfully create user with email {user_dict['email']}",
			status=200
			), 200



