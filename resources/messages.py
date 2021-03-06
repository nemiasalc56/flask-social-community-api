# import our models
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from flask_socketio import SocketIO, send, emit



# the first messages is the blueprint name
# the second is the its import_name
messages = Blueprint('messages', 'messages')





# message index route
@messages.route('/<group_id>', methods=['GET'])
@login_required
def message_index(group_id):

	# look up messages with the same group id
	messages = models.Message.select()

	# convert group id to integer
	id = int(group_id)

	message_dicts = [model_to_dict(message) for message in messages if message.group_fk.id == id]

	# remove the passwords
	for message in message_dicts:
		message['owner_fk'].pop('password')
		message['group_fk']['owner_fk'].pop('password')


	return jsonify(
		data=message_dicts,
		messages=f"Succesfully retrieved {len(message_dicts)} messages",
		status=200
		), 200



# create POST route
@messages.route('/<group_id>', methods=['POST'])
@login_required
def send_message(group_id):

	# get the message from the request
	payload = request.get_json()

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
			), 200



# delete route
@messages.route('/<id>', methods=['Delete'])
@login_required
def delete(id):

	# look up message to delete
	message_to_delete = models.Message.get_by_id(id)
	message_dict = model_to_dict(message_to_delete)
	# check if the user is the owner of the message
	if current_user.id == message_dict['owner_fk']['id']:

		# delete message
		message_to_delete.delete_instance(recursive=True)

		return jsonify(
			data={},
			message="Succesfully delete message",
			status=200
			), 200
	else:
		return jsonify(
			data={},
			message="You must be the owner to delete this message",
			status=200
			), 200




