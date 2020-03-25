# import models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user



# the first groups is the blueprint name
# the second argument is its import_name
groups = Blueprint('groups', 'groups')




# GET groups index
@groups.route('/', methods=['GET'])
def group_index():

	# loop up groups that belongs to current logged in user
	current_user_groups = [model_to_dict(group) for group in current_user.groups]

	# remove user password before returning the information
	for group in current_user_groups:
		group['owner_fk'].pop('password')

	print(current_user_groups)


	return jsonify(
		data=current_user_groups,
		message=f"Successfuly retrieved {len(current_user_groups)} groups",
		status=200
		), 200



# GET group show route
@groups.route('/<id>', methods=['GET'])
def get_one_group(id):
	print(id)

	return "You hit the group show route"





# POST create route
@groups.route('/', methods=['POST'])
def make_group():
	# get the info from the request
	payload = request.get_json()
	print(payload)

	new_group = models.Group.create(
		name = payload['name'],
		owner_fk = payload['owner_fk']
		)
	
	# remove user password
	group_dict = model_to_dict(new_group)
	group_dict['owner_fk'].pop('password')

	print(group_dict)

	return jsonify(
		data=group_dict,
		message="Successfuly craeted group",
		status=200
		), 200




