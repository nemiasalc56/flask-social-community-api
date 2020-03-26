import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user


# the first members is the blueprint name
# the second argument is its import_name
members = Blueprint('members', 'members')



# member index route
@members.route('/<group_id>', methods=['GET'])
def member_index(group_id):

	id = int(group_id)
	print(type(id))
	# look up member that are in that group
	members = models.Member.select()

	member_dicts = [model_to_dict(member) for member in members if member.group_fk == id]
	print(member_dicts)

	return jsonify(
		data=member_dicts,
		message=f"Succesfully retrieved {len(member_dicts)} members",
		status=200
		), 200





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


# members delete route
@members.route('/<id>', methods=['Delete'])
def delete(id):

	print(id)

	return "You hit the member delete route"


