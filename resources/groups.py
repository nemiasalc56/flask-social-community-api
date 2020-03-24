# import models and blueprint
import models
from flask import Blueprint, request



# the first groups is the blueprint name
# the second argument is its import_name
groups = Blueprint('groups', 'groups')






# POST create route
@groups.route('/', methods=['POST'])
def make_group():

	return "You hit the groups create route"