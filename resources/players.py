# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


players = Blueprint('players', 'players')



# player index route
@players.route('/<group_id>', methods=['GET'])
@login_required
def player_index(group_id):

	player = models.Player.select()
	player_dict = [model_to_dict(video) for video in player if video.group_fk.id == int(group_id)]

	for video in player_dict:
		video['group_fk']['owner_fk'].pop('password')

	return jsonify(
		data=player_dict,
		message="Succefully found the video playing.",
		status=200
		), 200





# create route
@players.route('/<group_id>', methods=['POST'])
@login_required
def player(group_id):

	# get the information from the request
	payload = request.get_json()

	video = models.Player.create(
		name=payload['name'],
		group_fk=group_id
		)

	video_dict = model_to_dict(video)
	# remove the owner's password
	video_dict['group_fk']['owner_fk'].pop('password')

	return jsonify(
		data=video_dict,
		message="Succefully created video",
		status=200
		), 200






