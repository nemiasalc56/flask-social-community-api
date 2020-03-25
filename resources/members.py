import models
from flask import Blueprint, request



# the first members is the blueprint name
# the second argument is its import_name
members = Blueprint('members', 'members')


# members create route
@members.route('/', methods=['POST'])
def add_member():

	payload = request.get_json()

	print(payload)

	return "You hit the member create route"