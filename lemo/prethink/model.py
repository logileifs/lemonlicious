import logging
import ujson as json
import rethinkdb as r
#from rethinkdb import errors as rt_errors
from six import add_metaclass

import marshmallow
from marshmallow import Schema
from marshmallow.fields import Field as BaseField
from lemo.prethink.connection import get_connection

log = logging.getLogger(__name__)


class BaseModel(type):
	def __new__(cls, clsname, bases, dct):
		#print('cls: %s' % cls)
		#print('clsname: %s' % clsname)
		#print('bases: %s' % bases)
		#print('dct: %s' % dct)
		super_new = super(BaseModel, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)

		#new_class._fields = dct.get('_fields', OrderedDict())
		# everything that is passed to the class and does not start with double
		# underscore we treat as a database field and set it to the _fields dict
		#new_class._fields = {
		#	key: value for key, value in dct.items() if not key.startswith('__')
		#}

		new_class._fields = {}
		#new_class._data = {}
		#print('dct.items()')
		for key, value in dct.items():
			if not key.startswith('__'):
				new_class._fields[key] = value
				print('new_class._fields[%s] = %s' % (key, value))
				#print(value)
				#if isinstance(value, BaseField):
				#	#print('is BaseField')
				#	new_class._data[key] = None
				#else:
				#	new_class._data[key] = value
		#new_class._data['id'] = None

		#new_class._data = {
		#	key: None for key, value in dct.items() if not key.startswith('__')
		#}
		# set table name to clsname, maybe switch to inflection here
		# https://inflection.readthedocs.io/en/latest/#inflection.tableize
		new_class._table = clsname
		new_class._table_exists = False

		new_class._schema = type(
			'UserSchema2',
			(Schema,),
			new_class._fields
		)

		print('new_class._fields')
		print(new_class._fields)
		return new_class


@add_metaclass(BaseModel)
class Model(object):
	def __init__(self, **kwargs):
		self.__dict__['_data'] = {}
		#if data:
		#	for key, value in data.items():
		#		setattr(self, key, value)
		for key, value in self._fields.items():
			if isinstance(value, BaseField):
				self._data[key] = None
			else:
				self._data[key] = value
		for key, value in kwargs.items():
			# Assign fields this way to be sure that validation takes place
			setattr(self, key, value)
		# if id has not been supplied we set it to None
		#if 'id' not in self._data:
		#	self._data['id'] = None
		log.debug('new Model created with data: %s' % self._fields)

	def __setattr__(self, key, value):
		log.debug('setattr %s: %s' % (key, value))
		# check if we have a field called *key
		field = self._fields.get(key, None)
		log.debug('field: %s' % field)
		# only set the value if there is a defined field for it
		if field is not None:
			#field.validate(value)
			#field_dict = {}
			try:
				self._schema.load({field: value}, partial=True)
			except marshmallow.exceptions.ValidationError:
				log.exception('marshmallow ValidationError')
			# validate the value here
			self._data[key] = value
		elif key == 'id':
			#print('set id')
			self._data['id'] = value

	def __getattr__(self, key):
		field = self._fields.get(key)
		if field or key == 'id':
			return self._data.get(key)
		raise AttributeError("'Model' object has no attribute '%s'" % key)

	def __repr__(self):
		return '<%s object>' % self.__class__.__name__

	@classmethod
	def all(cls):
		#users = list(r.table("authors").run())
		connection = get_connection()
		table = r.table(cls._table)
		try:
			#table = db.rt.table(cls.table).run()
			return list(table.run(connection))
		except r.errors.ReqlOpFailedError:
			return []

	#@classmethod
	#def all(cls, raw=False):
	#	connection = get_connection()
	#	table = r.table(cls._table)
	#	result = next(table.run(connection))
	#	if raw:
	#		yield result
	#	else:
	#		yield cls(**result)

	@classmethod
	def get(cls, _id, raw=False):
		connection = get_connection()
		table = r.table(cls._table)
		result = table.get(_id).run(connection)
		if raw:
			return result
		else:
			return cls(**result)

	@classmethod
	def filter(cls, filters, raw=False):
		connection = get_connection()
		table = r.table(cls._table)
		result = next(table.filter(filters).run(connection))
		if raw:
			yield result
		else:
			yield cls(**result)

	@property
	def data(self):
		log.debug('data: %s' % self._data)
		return self._data

	def dump(self):
		print(self._data)
		return json.dumps(self._data)

	def get_table(self):
		table = r.table(self._table)
		return table

	def create_table(self):
		connection = get_connection()
		r.table_create(self._table).run(connection)

	def _do_insert(self):
		connection = get_connection()
		table = self.get_table()
		result = table.insert(self._data, return_changes=True).run(connection)
		errors = result['errors']
		if not errors:
			self._data['id'] = result['generated_keys'][0]
		return result

	def insert(self):
		try:
			result = self._do_insert()
		except r.errors.ReqlOpFailedError:
			self.create_table()
			result = self._do_insert()
		return result

	def _do_update(self):
		log.debug('do update')
		connection = get_connection()
		table = self.get_table()
		_id = self._data['id']
		log.debug('data: %s' % self._data)
		result = table.get(_id).update(
			self._data, non_atomic=True
		).run(connection)
		return result

	def update(self):
		try:
			result = self._do_update()
		except r.errors.ReqlOpFailedError:
			self.create_table()
			result = self._do_update()
		return result

	def delete(self):
		connection = get_connection()
		table = self.get_table()
		_id = self._data.get('id')
		if _id:
			result = table.get(_id).delete().run(connection)
			self._data.pop('id')
			return result

	def save(self):
		try:
			result = self.update()
		except KeyError:
			result = self.insert()

		return result
