# import our models
import models
from flask import Blueprint, request, jsonify


# the first messages is the blueprint name
# the second is the its import_name
messages = Blueprint('messages', 'messages')


# create POST route
@messages.route('/<group_id>', methods=['POST'])
def send_message(group_id):

	payload = request.get_json()

	print(group_id)
	print(payload)

	return "You hit the messages create route"