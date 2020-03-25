import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user


# the first members is the blueprint name
# the second argument is its import_name
members = Blueprint('members', 'members')


# members create route
@members.route('/', methods=['POST'])
def add_member():

	payload = request.get_json()
	print(payload)

	# look up group
	group = models.Group.get_by_id(payload['group_fk'])
	print(group)

	# look up member
	member = models.Member.create(
		group_fk = payload['group_fk'],
		member_fk = payload['member_fk']
		)

	member_dict = model_to_dict(member)
	member_dict['group_fk']['owner_fk'].pop('password')
	member_dict['member_fk'].pop('password')
	print(member_dict)


	return jsonify(
		data=member_dict,
		message="Succesfully create member",
		status=200
		), 200





