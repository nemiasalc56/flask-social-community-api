# import our models
import models
from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict



# the first messages is the blueprint name
# the second is the its import_name
messages = Blueprint('messages', 'messages')


# create POST route
@messages.route('/<group_id>', methods=['POST'])
def send_message(group_id):

	# get the message from the request
	payload = request.get_json()
	print(payload)
	print(group_id)

	if payload['message'] != "":
		message = models.Message.create(
			message=payload['message'],
			owner_fk=current_user.id,
			group_fk=group_id
			)

		# conert to dictionary
		message_dict = model_to_dict(message)

		# remove user password
		message_dict['owner_fk'].pop('password')
		message_dict['group_fk']['owner_fk'].pop('password')
		print(message_dict)

		return jsonify(
			data=message_dict,
			message="Succesfully create message",
			status=200
			), 200
	else:
		return jsonify(
			data={},
			message="You must type something to create a message",
			status=401
			), 401






