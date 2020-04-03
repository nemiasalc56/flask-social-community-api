## Social Community

An app the users can chat and create group chat. A user will be able to create a group and search for a video or music that everyone in the group will be watching at the same time and the will be able to keep chatting in the group at the same time.

## User stories

* User can create a group to chat
* User can select a video to watch if the group was created
* User can delete a group

## Installation

* ```$ virtualenv .env -p python3```
* ```$ source .env/bin/activate```
* ```$ pip3 install virtualenv```
* ```$ pip3 install flask```
* ```$ pip3 install peewee psycopg2```
* ```$ pip3 freeze > requirements.txt```
* ```$ pip3 install flask_login flask-bcrypt```
* ```$ pip3 install flask-socketio```


## Models 
```
class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password = CharField()



class Group(Model):
	name = CharField()
	owner_fk = ForeignKeyField(User, backref='groups')
	secondary_user_fk = CharField()


class Member(Model):
	group_fk = ForeignKeyField(Group, backref='members')
	member_fk = ForeignKeyField(User, backref='members')


class Chat(Model):
	message = CharField()
	owner_fk = ForeignKeyField(User, backref='chats')
	group_fk = ForeignKeyField(Group, backref='chats')
	created_at = DateTimeField(default=datetime.datetime.now)



class Player(Model):
	name = CharField()
	group_fk = ForeignKeyField(Group, backref='player')
```

## API Routes

-- User
| HTTP method | URL path | Description |
| -----------:|:--------:| ----------:|
| GET | `/users` | list of users |
| POST | `/users/register` | register user |
| POST | `/users/login` | log user in |
| GET | `/users/logout` | log user out |
| PUT | `/users/<id>` | update user |
| DELETE | `/users/<id>` | delete user |


-- Group
| HTTP method | URL path | Description|
| -----------:|:--------:| ----------:|
| GET | `/groups` | list of groups |
| GET | `/groups/<id>` | show a group |
| POST | `/groups` | create a group |
| PUT | `'/groups/<id>' | update a group |
| DELETE | `/groups/<id>` | delete a group |


-- Member
| HTTP method | URL path | Description|
| -----------:|:--------:| ----------:|
| GET | `/members` | list of members |
| POST | `/members` | add a member |
| PUT | `'/members/<id>' | update a member |
| DELETE | `/members/<id>` | delete a member |


-- Chat
| HTTP method | URL path | Description|
| -----------:|:--------:| ----------:|
| GET | `/messages` | list of messages |
| POST | `/messages` | create a message |
| PUT | `'/messages/<id>' | update a message |
| DELETE | `/messages/<id>` | delete a message |





## Technology Used

* Youtube API
* Cloudinary
* Python
* Flask
* React
* Socket.io
