# import everything from peewee
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect




# using sqlite to have a database
DATABASE = SqliteDatabase('communities.sqlite')





# defining our tables
class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password = CharField()

	# this gives our class instructions on how to connect to a specific database
	class Meta:
		database = DATABASE



class Group(Model):
	name = CharField()
	owner_fk = ForeignKeyField(User, backref='groups')

	class Meta:
		database = DATABASE


# this is our group member
class Member(Model):
	group_fk = ForeignKeyField(Group, backref='members')
	member_fk = ForeignKeyField(User, backref='members')

	class Meta:
		database = DATABASE



class Message(Model):
	message = CharField()
	owner_fk = ForeignKeyField(User, backref='chats')
	group_fk = ForeignKeyField(Group, backref='chats')
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE



class Player(Model):
	name = CharField()
	group_fk = ForeignKeyField(Group, backref='player')

	class Meta:
		database = DATABASE



# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Group, Member, Message, Player], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()