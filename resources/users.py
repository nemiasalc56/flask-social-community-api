# import models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user




# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# user index route
@users.route('/', methods=['GET'])
def index():

	return "You hit the users index route"



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
	
		# log user in
		login_user(new_user)

		# convert mode to dictionary
		user_dict = model_to_dict(new_user)
		print(user_dict)

		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"Succesfully create user with email {user_dict['email']}",
			status=200
			), 200



# login route
@users.route('/login', methods=['POST'])
def login():

	payload = request.get_json()
	print(payload)

	# convert email to lower case
	payload['email'] = payload['email'].lower()

	try:

		# look up user by email
		user = models.User.get(models.User.email == payload['email'])
		# this should cause an error if the user doesn't exist

		user_dict = model_to_dict(user)

		# check if the password is correct
		password_is_good = check_password_hash(user_dict['password'], payload['password'])
		# if the password is good, log user in
		if password_is_good:
			# this logs the user and starts a new session
			login_user(user)
			print("here")

			# remove the password
			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message=f"Succesfully logged in user with email {user_dict['email']}",
				status=200
				), 200

		# if not, inform the user that the email or password is incorrect
		else:

			return jsonify(
				data={},
				message="The email or password is incorrect",
				status=401
				), 401
	# if we don't find the user
	except models.DoesNotExist:
		# inform the user that the email or password is incorrect
		return jsonify(
				data={},
				message="The email or password is incorrect",
				status=401
				), 401



# loguot route
@users.route('/logout', methods=['GET'])
def logout():
	# this is to log user out
	logout_user()
	return jsonify(
		data={},
		message="Succesfully logout.",
		status=200
		), 200

# update route
@users.route('/<id>', methods=['PUT'])
def update(id):
	# get the info from the body
	payload = request.get_json()
	print(payload)
	print(id)

	# look up user with the same id
	user = models.User.get_by_id(id)
	print(user.first_name)

	user.first_name = payload['first_name'] if 'first_name' in payload else None
	user.last_name = payload['last_name'] if 'last_name' in payload else None
	user.picture = payload['picture'] if 'picture' in payload else None
	user.password = payload['password'] if 'password' in payload else None
	user.save()

	# convert model to dictionary
	user_dict = model_to_dict(user)

	return jsonify(
		data=user_dict,
		message="Succesfully update user information",
		status=200
		), 200







