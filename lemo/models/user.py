#import rethinkdb as r
#r.connect('localhost', 28015).repl()
#r.db('test').table_create('tv_shows').run()
#r.table('tv_shows').insert({ 'name': 'Star Trek TNG' }).run()
import uuid
from lemo import db
from lemo import config
from lemo.prethink import Model
from lemo.prethink import connect
#from marshmallow import Schema
from marshmallow import fields

cfg = config.load()
#conn = db.connect(host=cfg['db_host'], port=cfg['db_port'])
connect(host=cfg['db_host'], port=cfg['db_port'])


class User(Model):

	#table = 'users'

	#class UserSchema(Schema):
	name = fields.Str(required=True)
	email = fields.Email(required=True)
	#created_at = fields.DateTime()

	#def __init__(self, **data):
	#	self.UserSchema().load(data)
	#	self.id = str(uuid.uuid4())
	#	self.data = data
	#	data['id'] = self.id

	#def save(self):
	#	try:
	#		db.rt.table(self.table).run()
	#	except db.rt.errors.ReqlOpFailedError:
	#		db.rt.table_create(self.table).run()
	#	db.rt.table(self.table).insert(self.data).run()

	#@classmethod
	#def all(cls):
	#	#users = list(r.table("authors").run())
	#	#connection = get_connection()
	#	try:
	#		#table = db.rt.table(cls.table).run()
	#		return list(db.rt.table(cls.table).run(conn))
	#	except db.rt.errors.ReqlOpFailedError:
	#		return []
