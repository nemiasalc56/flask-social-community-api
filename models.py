import os
# import everything from peewee
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on

else:
	# using sqlite to have a database
	# this will allow us to use cascading delete
	DATABASE = SqliteDatabase('communities.sqlite', pragmas={'foreign_keys': 1})





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
	owner_fk = ForeignKeyField(User, backref='groups', on_delete='CASCADE')

	class Meta:
		database = DATABASE


# this is our group member
class Member(Model):
	group_fk = ForeignKeyField(Group, backref='members', on_delete='CASCADE')
	member_fk = ForeignKeyField(User, backref='members', on_delete='CASCADE')

	class Meta:
		database = DATABASE



class Message(Model):
	message = CharField()
	owner_fk = ForeignKeyField(User, backref='chats')
	group_fk = ForeignKeyField(Group, backref='chats', on_delete='CASCADE')
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE



class Video(Model):
	name = CharField()
	group_fk = ForeignKeyField(Group, backref='player')

	class Meta:
		database = DATABASE



# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Group, Member, Message, Video], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()