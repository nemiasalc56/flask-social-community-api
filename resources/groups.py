# import models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict



# the first groups is the blueprint name
# the second argument is its import_name
groups = Blueprint('groups', 'groups')




# POST create route
@groups.route('/', methods=['POST'])
def make_group():
	# get the info from the request
	payload = request.get_json()
	print(payload)

	group_member = models.Group.create(
		name = payload['name'],
		owner_fk = payload['owner_fk'],
		secondary_user_fk = payload['secondary_user_fk']
		)
	
	# remove user password
	group_member_dict = model_to_dict(group_member)
	group_member_dict['owner_fk'].pop('password')

	print(group_member_dict)

	return jsonify(
		data=group_member_dict,
		message="Successfuly craeted group",
		status=200
		), 200

