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
	print(id)
	# look up member that are in that group
	members = models.Member.select()
	print(members)
	member_dicts = [model_to_dict(member) for member in members if member.group_fk.id == id]
	print(member_dicts)

	# remove the members' password
	for member in member_dicts:
		print('\n')
		member['group_fk']['owner_fk'].pop('password')
		member['member_fk'].pop('password')

	return jsonify(
		data=member_dicts,
		message=f"Succesfully retrieved {len(member_dicts)} members",
		status=200
		), 200





# members create route
@members.route('/', methods=['POST'])
def add_member():

	payload = request.get_json()
	group_id = int(payload['group_fk'])
	member_id = int(payload['member_fk'])

	# check if the member is in the group
	# if it does, infom that member already exist
	members = models.Member.select()

	member_in_group_dicts = [model_to_dict(member) for member in members if member.group_fk.id == group_id]
	print(len(member_in_group_dicts))
	# if we don't find a group, we can add the member
	if len(member_in_group_dicts) == 0:
		print('heee')
		# create member
		member = models.Member.create(
			group_fk = payload['group_fk'],
			member_fk = payload['member_fk']
			)

		member_dict = model_to_dict(member)
		member_dict['group_fk']['owner_fk'].pop('password')
		member_dict['member_fk'].pop('password')
		# print(member_dict)


		return jsonify(
			data=member_dict,
			message="Succesfully create member",
			status=200
			), 200

	else:

		member_exist = False

		# check if the user is in the group already
		for member in member_in_group_dicts:
			print("printing member")
			print(type(member["member_fk"]["id"]))
			print("printing id")
			print(group_id)

			if member["member_fk"]["id"] == member_id:
				print(member["member_fk"])
				member_exist = True

		print(member_exist)
		if member_exist == True:
			
			return jsonify(
				data={},
				message="member already exist",
				status=401
				), 401


		elif member_exist == False:

			# create member
			member = models.Member.create(
				group_fk = payload['group_fk'],
				member_fk = payload['member_fk']
				)

			member_dict = model_to_dict(member)
			member_dict['group_fk']['owner_fk'].pop('password')
			member_dict['member_fk'].pop('password')
			# print(member_dict)


			return jsonify(
				data=member_dict,
				message="Succesfully create member",
				status=200
				), 200

		


# members delete route
@members.route('/<id>', methods=['Delete'])
def delete(id):

	# loop up member with the same id
	member_to_delete = models.Member.get_by_id(id)
	print(model_to_dict(member_to_delete))

	# delete member
	member_to_delete.delete_instance()


	return jsonify(
		data={},
		message=f"Succesfully delete member with id {id}",
		status=200
		), 200


