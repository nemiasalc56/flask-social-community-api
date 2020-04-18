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

	try:

		# loop up groups that belongs to current logged in user
		current_user_groups = [model_to_dict(group) for group in current_user.groups]
		current_user_members = [model_to_dict(member) for member in current_user.members]

		for member in current_user_members:
			current_user_groups.append(member['group_fk'])


		# remove user password before returning the information
		for group in current_user_groups:
			group['owner_fk'].pop('password')

		# print(current_user_groups)


		return jsonify(
			data=current_user_groups,
			message=f"Successfuly retrieved {len(current_user_groups)} groups",
			status=200
			), 200

	except:
		return jsonify(
			data={},
			message="You don't have groups",
			status=401
			), 401



# GET group show route
@groups.route('/<id>', methods=['GET'])
def get_one_group(id):
	print(id)
	try:
		group = models.Group.get_by_id(id)
		group_dict = model_to_dict(group)

		# remove the owner's password
		group_dict['owner_fk'].pop('password')

		return jsonify(
			data=group_dict,
			message=f"Successfuly found group with the id {id}",
			status=200
			), 200

	except models.DoesNotExist:
		return jsonify(
			data={},
			message="You don't have a group with this id",
			status=401
			), 401





# POST create route
@groups.route('/', methods=['POST'])
def make_group():
	# get the info from the request
	payload = request.get_json()

	new_group = models.Group.create(
		name = payload['name'],
		owner_fk = current_user.id
		)
	
	# remove user password
	group_dict = model_to_dict(new_group)
	group_dict['owner_fk'].pop('password')


	return jsonify(
		data=group_dict,
		message="Successfuly craeted group",
		status=200
		), 200


# update route
@groups.route('/<id>', methods=['PUT'])
def update_group(id):
	payload = request.get_json()

	# look up group with the same id
	group_to_update = models.Group.get_by_id(id)

	# update the information
	group_to_update.name = payload['name'] if 'name' in payload else None
	group_to_update.save()

	# convert to dictionary
	group_dict = model_to_dict(group_to_update)
	# remove owner's password
	group_dict['owner_fk'].pop('password')


	return jsonify(
		data= group_dict,
		message="Successfuly update group",
		status=200
		), 200




# delete route
@groups.route('/<id>', methods=['Delete'])
def delete_group(id):

	# look up group to delete
	group = models.Group.get_by_id(id)

	group.delete_instance(recursive=True)


	return jsonify(
		data={},
		message=f"Successfuly deleted group with id {id}",
		status=200
		), 200



